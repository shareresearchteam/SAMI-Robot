import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE, ADASYN
import xgboost as xgb
import joblib
import wandb

# =========================
# CONFIG - TUNABLE PARAMETERS
# =========================

DATASET = 5

if DATASET == 0:
    DATA_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\clean"
    OUTPUT_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\results\xgboost"
elif DATASET == 1:
    DATA_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\clean2"
    OUTPUT_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\results\xgboost(2)"
elif DATASET == 2:
    DATA_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\clean3"
    OUTPUT_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\results\xgboost(3)"
elif DATASET == 3:
    DATA_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\clean4"
    OUTPUT_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\results\xgboost(4)"
else:
    DATA_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\clean5"
    OUTPUT_DIR = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\results\xgboost(5)"

os.makedirs(OUTPUT_DIR, exist_ok=True)

FILES = {
    "raw": "raw.csv",
}

FEATURE_SETS = {
    "full": ["pir_left", "pir_right", "us_left", "us_mid", "us_right"],
}

LABEL_COL = "yolo_total"


# ============== XGBOOST TUNING PARAMETERS ==============
TEST_SIZE = 0.3
RANDOM_STATE = 42

XGBOOST_PARAMS = {
    'max_depth': 12,
    'learning_rate': 0.2,
    'n_estimators': 2500,
    'min_child_weight': 1,
    'gamma': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'reg_alpha': 0.1,
    'reg_lambda': 1.0,
    'scale_pos_weight': 1.0,
    'objective': 'binary:logistic',
    'eval_metric': ['logloss', 'auc', 'error'],
    'use_label_encoder': False,
    'random_state': RANDOM_STATE,
    'n_jobs': -1,
    'tree_method': 'hist',
}

DECISION_THRESHOLD = 0.5
USE_SMOTE = False
SMOTE_STRATEGY = 0.5
USE_ADASYN = False
OPTIMIZE_METRIC = "f1"
EARLY_STOPPING_ROUNDS = 20


def find_best_threshold(y_probs, y_true):
    best_f1, best_t = 0, 0.5
    for t in np.linspace(0.1, 0.9, 81):
        preds = (y_probs > t).astype(int)
        report = classification_report(y_true, preds, output_dict=True, zero_division=0)
        f1 = report.get("1", {}).get("f1-score", 0)
        if f1 > best_f1:
            best_f1, best_t = f1, t
    return best_t, best_f1


def calculate_metrics(y_true, y_pred):
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    false_positives = np.sum((y_true == 0) & (y_pred == 1))
    actual_positives = np.sum(y_true == 1)
    recall = true_positives / actual_positives if actual_positives > 0 else 0
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

resampler_name = "adasyn" if USE_ADASYN else "smote" if USE_SMOTE else "no_resample"


# =========================
# WANDB INIT (can comment out if no need for this)
# =========================

wandb.login()
run = wandb.init(
    project="capstone-xgboost",
    name=f"dataset{DATASET}_{resampler_name}_{OPTIMIZE_METRIC}",
    config={
        "dataset": DATASET,
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
        "optimize_metric": OPTIMIZE_METRIC,
        "early_stopping_rounds": EARLY_STOPPING_ROUNDS,
        "use_smote": USE_SMOTE,
        "use_adasyn": USE_ADASYN,
        "smote_strategy": SMOTE_STRATEGY,
        **{f"xgb_{k}": v for k, v in XGBOOST_PARAMS.items() if not isinstance(v, list)},
    }
)

# =========================
# PIPELINE
# =========================
results = []
model_artifacts = []
evals_result = {}

for name, file in FILES.items():
    path = os.path.join(DATA_DIR, file)

    if not os.path.exists(path):
        print(f"Skipping missing file: {file}")
        continue

    df = pd.read_csv(path)

    if LABEL_COL not in df.columns:
        print(f"Skipping {file} (no label column)")
        continue

    y = (df[LABEL_COL] > 0).astype(int).values

    for feat_name, features in FEATURE_SETS.items():
        if not all(col in df.columns for col in features):
            continue

        print(f"\n{'='*70}")
        print(f"Dataset: {name} | Features: {feat_name}")
        print(f"{'='*70}")

        X = df[features].values

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train_full, X_test, y_train_full, y_test = train_test_split(
            X_scaled, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_full, y_train_full, test_size=0.2, random_state=RANDOM_STATE
        )

        # Log class distribution
        wandb.log({
            "data/train_class0": int(np.sum(y_train == 0)),
            "data/train_class1": int(np.sum(y_train == 1)),
            "data/test_class0": int(np.sum(y_test == 0)),
            "data/test_class1": int(np.sum(y_test == 1)),
            "data/class_ratio": float(np.sum(y_train == 0) / max(np.sum(y_train == 1), 1)),
        })

        if USE_SMOTE:
            print(f"Before resampling - Class 0: {np.sum(y_train == 0)}, Class 1: {np.sum(y_train == 1)}")
            if USE_ADASYN:
                resampler = ADASYN(sampling_strategy=SMOTE_STRATEGY, random_state=RANDOM_STATE, n_neighbors=5)
                resample_label = "ADASYN"
            else:
                resampler = SMOTE(sampling_strategy=SMOTE_STRATEGY, random_state=RANDOM_STATE)
                resample_label = "SMOTE"
            X_train, y_train = resampler.fit_resample(X_train, y_train)
            print(f"After {resample_label} - Class 0: {np.sum(y_train == 0)}, Class 1: {np.sum(y_train == 1)}")
            wandb.log({
                "data/resampled_class0": int(np.sum(y_train == 0)),
                "data/resampled_class1": int(np.sum(y_train == 1)),
            })

        class_counts = np.bincount(y_train)
        scale_pos_weight = class_counts[0] / class_counts[1] if class_counts[1] > 0 else 1.0
        print(f"Calculated scale_pos_weight: {scale_pos_weight:.2f}")

        params = XGBOOST_PARAMS.copy()
        params['scale_pos_weight'] = scale_pos_weight

        dtrain = xgb.DMatrix(X_train, label=y_train)
        dval   = xgb.DMatrix(X_val,   label=y_val)
        dtest  = xgb.DMatrix(X_test,  label=y_test)

        class WandbCallback(xgb.callback.TrainingCallback):
            def after_iteration(self, model, epoch, evals_log):
                log_dict = {"train/round": epoch}
                for dataset, metrics in evals_log.items():
                    for metric, values in metrics.items():
                        log_dict[f"{dataset}/{metric}"] = values[-1]
                wandb.log(log_dict)
                return False 

        print(f"\nTraining XGBoost (optimizing {OPTIMIZE_METRIC})...")
        evals = [(dtrain, 'train'), (dval, 'validation')]

        model = xgb.train(
            params,
            dtrain,
            num_boost_round=params['n_estimators'],
            evals=evals,
            early_stopping_rounds=EARLY_STOPPING_ROUNDS,
            evals_result=evals_result,
            callbacks=[WandbCallback()],
            verbose_eval=10,
        )

        print(f"\nBest iteration: {model.best_iteration}")
        print(f"Best score: {model.best_score:.4f}")

        wandb.log({
            "training/best_iteration": model.best_iteration,
            "training/best_score": model.best_score,
            "training/scale_pos_weight": scale_pos_weight,
        })

        # Threshold optimisation on validation set
        val_probs = model.predict(dval)
        best_threshold, best_val_f1 = find_best_threshold(val_probs, y_val)
        print(f"\nOptimal threshold: {best_threshold:.3f} | Val F1: {best_val_f1:.4f}")

        wandb.log({
            "threshold/best_threshold": best_threshold,
            "threshold/best_val_f1": best_val_f1,
        })

        # Test evaluation
        y_probs = model.predict(dtest)
        y_pred  = (y_probs > best_threshold).astype(int)

        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        acc    = accuracy_score(y_test, y_pred)

        print(f"\n{'='*70}")
        print(f"TEST RESULTS (threshold={best_threshold:.3f})")
        print(f"{'='*70}")
        print(f"Test Accuracy: {acc:.4f}")
        print(f"Test Recall    (Class 1): {report.get('1', {}).get('recall',    0):.4f}")
        print(f"Test Precision (Class 1): {report.get('1', {}).get('precision', 0):.4f}")
        print(f"Test F1        (Class 1): {report.get('1', {}).get('f1-score',  0):.4f}")
        print("\nFull Classification Report:")
        print(classification_report(y_test, y_pred, target_names=["No Person", "Person Present"], zero_division=0))

        # Log all test metrics to wandb
        wandb.log({
            "test/accuracy":    acc,
            "test/recall":      report.get("1", {}).get("recall",    0),
            "test/precision":   report.get("1", {}).get("precision", 0),
            "test/f1":          report.get("1", {}).get("f1-score",  0),
            "test/recall_0":    report.get("0", {}).get("recall",    0),
            "test/precision_0": report.get("0", {}).get("precision", 0),
            "test/f1_0":        report.get("0", {}).get("f1-score",  0),
        })

        # Confusion matrix in wandb
        wandb.log({
            "test/confusion_matrix": wandb.plot.confusion_matrix(
                probs=None,
                y_true=y_test.tolist(),
                preds=y_pred.tolist(),
                class_names=["No Person", "Person Present"],
            )
        })

        # ROC curve
        wandb.log({
            "test/roc_curve": wandb.plot.roc_curve(
                y_test,
                np.column_stack([1 - y_probs, y_probs]),
                labels=["No Person", "Person Present"],
            )
        })

        # PR curve
        wandb.log({
            "test/pr_curve": wandb.plot.pr_curve(
                y_test,
                np.column_stack([1 - y_probs, y_probs]),
                labels=["No Person", "Person Present"],
            )
        })

        # Feature importance
        importance = model.get_score(importance_type='gain')
        print("\nFeature Importance (gain):")
        feat_importance_data = []
        for feat_idx, feat in enumerate(features):
            feat_key = f"f{feat_idx}"
            imp_value = importance.get(feat_key, 0)
            print(f"  {feat}: {imp_value:.2f}")
            feat_importance_data.append([feat, imp_value])
            wandb.log({f"feature_importance/{feat}": imp_value})

        # Feature importance bar chart in wandb
        fi_table = wandb.Table(data=feat_importance_data, columns=["feature", "importance_gain"])
        wandb.log({
            "feature_importance/chart": wandb.plot.bar(fi_table, "feature", "importance_gain", title="Feature Importance (Gain)")
        })

        model_artifacts.append({
            'model': model,
            'scaler': scaler,
            'features': features,
            'dataset': name,
            'feature_set': feat_name,
            'f1_score': report.get('1', {}).get('f1-score', 0),
            'threshold': best_threshold,
        })

        results.append({
            "dataset": name,
            "features": feat_name,
            "accuracy": acc,
            "threshold": best_threshold,
            "best_iteration": model.best_iteration,
            "precision_0": report.get("0", {}).get("precision", 0),
            "recall_0":    report.get("0", {}).get("recall",    0),
            "f1_0":        report.get("0", {}).get("f1-score",  0),
            "support_0":   report.get("0", {}).get("support",   0),
            "precision_1": report.get("1", {}).get("precision", 0),
            "recall_1":    report.get("1", {}).get("recall",    0),
            "f1_1":        report.get("1", {}).get("f1-score",  0),
            "support_1":   report.get("1", {}).get("support",   0),
        })

# =========================
# SAVE BEST MODEL ONLY
# =========================
if model_artifacts:
    best_artifact = max(model_artifacts, key=lambda x: x['f1_score'])

    print("\n" + "="*70)
    print("SAVING BEST MODEL")
    print("="*70)
    print(f"  Dataset:   {best_artifact['dataset']}")
    print(f"  Features:  {best_artifact['feature_set']}")
    print(f"  F1 Score:  {best_artifact['f1_score']:.4f}")
    print(f"  Threshold: {best_artifact['threshold']:.3f}")

    model_path = os.path.join(OUTPUT_DIR, "xgboost_best_model.json")
    best_artifact['model'].save_model(model_path)

    scaler_path = os.path.join(OUTPUT_DIR, "scaler_best_model.pkl")
    joblib.dump(best_artifact['scaler'], scaler_path)

    metadata = {
        'dataset':      best_artifact['dataset'],
        'feature_set':  best_artifact['feature_set'],
        'features':     best_artifact['features'],
        'f1_score':     best_artifact['f1_score'],
        'threshold':    best_artifact['threshold'],
    }
    metadata_path = os.path.join(OUTPUT_DIR, "best_model_metadata.pkl")
    joblib.dump(metadata, metadata_path)

    wandb.summary["best/dataset"]    = best_artifact['dataset']
    wandb.summary["best/feature_set"] = best_artifact['feature_set']
    wandb.summary["best/f1_score"]   = best_artifact['f1_score']
    wandb.summary["best/threshold"]  = best_artifact['threshold']

    artifact = wandb.Artifact(name="xgboost_best_model", type="model")
    artifact.add_file(model_path)
    artifact.add_file(scaler_path)
    artifact.add_file(metadata_path)
    run.log_artifact(artifact)

    print(f"\nSaved model, scaler, and metadata to: {OUTPUT_DIR}")




# =========================
# SAVE RESULTS 
# =========================
results_df = pd.DataFrame(results)
results_csv = os.path.join(OUTPUT_DIR, f"xgboost_{resampler_name}_{OPTIMIZE_METRIC}_results.csv")
results_df.to_csv(results_csv, index=False)

# Log results table to wandb
wandb.log({"results/summary_table": wandb.Table(dataframe=results_df)})

print("\n" + "="*70)
print(f"FINAL RESULTS - SORTED BY F1 SCORE")
print("="*70)
print(results_df.sort_values("f1_1", ascending=False))



# =========================
# PLOT METRICS (local + wandb)
# =========================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
labels  = results_df["dataset"] + " | " + results_df["features"]
x_pos   = np.arange(len(labels))

axes[0, 0].bar(x_pos, results_df["recall_1"],    color='green',  alpha=0.7)
axes[0, 0].set_xticks(x_pos); axes[0, 0].set_xticklabels(labels, rotation=45, ha="right")
axes[0, 0].set_ylabel("Recall (Class 1)");    axes[0, 0].set_title("Recall for Person Detection");    axes[0, 0].grid(axis='y', alpha=0.3)

axes[0, 1].bar(x_pos, results_df["precision_1"], color='orange', alpha=0.7)
axes[0, 1].set_xticks(x_pos); axes[0, 1].set_xticklabels(labels, rotation=45, ha="right")
axes[0, 1].set_ylabel("Precision (Class 1)"); axes[0, 1].set_title("Precision for Person Detection"); axes[0, 1].grid(axis='y', alpha=0.3)

axes[1, 0].bar(x_pos, results_df["f1_1"],        color='purple', alpha=0.7)
axes[1, 0].set_xticks(x_pos); axes[1, 0].set_xticklabels(labels, rotation=45, ha="right")
axes[1, 0].set_ylabel("F1 Score (Class 1)");  axes[1, 0].set_title("F1 Score for Person Detection");  axes[1, 0].grid(axis='y', alpha=0.3)

axes[1, 1].bar(x_pos, results_df["accuracy"],    color='blue',   alpha=0.7)
axes[1, 1].set_xticks(x_pos); axes[1, 1].set_xticklabels(labels, rotation=45, ha="right")
axes[1, 1].set_ylabel("Accuracy");            axes[1, 1].set_title("Overall Accuracy");               axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plot_path = os.path.join(OUTPUT_DIR, f"xgboost_{resampler_name}_{OPTIMIZE_METRIC}_metrics.png")
plt.savefig(plot_path, dpi=300, bbox_inches='tight')
wandb.log({"charts/metrics_comparison": wandb.Image(plot_path)})
plt.close()

# =========================
# PLOT TRAINING (local + wandb)
# =========================
if evals_result:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    train_loss = evals_result['train']['logloss']
    val_loss   = evals_result['validation']['logloss']
    train_auc  = evals_result['train']['auc']
    val_auc    = evals_result['validation']['auc']
    epochs     = range(len(train_loss))

    axes[0].plot(epochs, train_loss, label='Training Loss',   color='blue',   alpha=0.7)
    axes[0].plot(epochs, val_loss,   label='Validation Loss', color='orange', alpha=0.7)
    axes[0].set_xlabel('Boosting Round'); axes[0].set_ylabel('Log Loss')
    axes[0].set_title('Training and Validation Loss'); axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].plot(epochs, train_auc, label='Training AUC',   color='blue',   alpha=0.7)
    axes[1].plot(epochs, val_auc,   label='Validation AUC', color='orange', alpha=0.7)
    axes[1].set_xlabel('Boosting Round'); axes[1].set_ylabel('AUC')
    axes[1].set_title('Training and Validation AUC'); axes[1].legend(); axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    history_path = os.path.join(OUTPUT_DIR, f"xgboost_{resampler_name}_training_history.png")
    plt.savefig(history_path, dpi=300, bbox_inches='tight')
    wandb.log({"charts/training_history": wandb.Image(history_path)})
    plt.close()

# =========================
# SUMMARY STATS
# =========================
print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)
print(f"Optimization metric: {OPTIMIZE_METRIC}")
print(f"Resampling method:   {resampler_name}")
print(f"\nAverage Metrics:")
print(f"  Recall:    {results_df['recall_1'].mean():.4f} ± {results_df['recall_1'].std():.4f}")
print(f"  Precision: {results_df['precision_1'].mean():.4f} ± {results_df['precision_1'].std():.4f}")
print(f"  F1 Score:  {results_df['f1_1'].mean():.4f} ± {results_df['f1_1'].std():.4f}")
print(f"  Accuracy:  {results_df['accuracy'].mean():.4f} ± {results_df['accuracy'].std():.4f}")

best_idx    = results_df['f1_1'].idxmax()
best_config = results_df.iloc[best_idx]
print(f"\nBest performing configuration:")
print(f"  Dataset:   {best_config['dataset']}")
print(f"  Features:  {best_config['features']}")
print(f"  F1 Score:  {best_config['f1_1']:.4f}")
print(f"  Recall:    {best_config['recall_1']:.4f}")
print(f"  Precision: {best_config['precision_1']:.4f}")
print(f"  Accuracy:  {best_config['accuracy']:.4f}")

wandb.finish()