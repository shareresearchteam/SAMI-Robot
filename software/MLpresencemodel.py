import xgboost as xgb
import numpy as np
import joblib

class PresenceModel:
    def __init__(self, model_path, scaler_path, metadata_path):
        self.model = xgb.Booster()
        self.model.load_model(model_path)

        self.scaler = joblib.load(scaler_path)
        self.metadata = joblib.load(metadata_path)

        self.threshold = self.metadata['threshold']
        self.features = self.metadata['features']

    def predict(self, sensor_dict):
        """
        sensor_dict must contain all required feature keys
        """
        X = np.array([[sensor_dict[feat] for feat in self.features]])
        X_scaled = self.scaler.transform(X)
        dmatrix = xgb.DMatrix(X_scaled)
        prob = self.model.predict(dmatrix)[0]
        pred = int(prob > self.threshold)
        return pred, prob


def parse_sensor_line(line):
    try:
        values = [v.strip() for v in line.split(',')]
        if len(values) < 7:
            return None

        return {
            'timestamp': float(values[0]),
            'pir_left': float(values[1]),
            'pir_right': float(values[2]),
            'us_left': float(values[3]),
            'us_mid': float(values[4]),
            'us_right': float(values[5]),
            'unknown': float(values[6])
        }
    except:
        return None