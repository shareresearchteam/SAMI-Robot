# ==============================================================================
# theme.py — Centralized design tokens for the SAMI UI.
#
# Every colour, font size, border radius, and spacing value used across
# the app lives here. Import what you need instead of hardcoding hex
# codes and pixel values in individual files.
#
# Usage:
#     from styles.theme import *          # grab everything
#     from styles.theme import BG_APP, TEXT_PRIMARY   # or pick and choose
# ==============================================================================


# ── Colour palette ────────────────────────────────────────────────────────────

# Background colours
BG_APP          = "#96C4DB"     # Main window / page background (light blue)
BG_CARD         = "#FFFFFF"     # Card / panel backgrounds
BG_BUTTON       = "#FFCCCC"     # Primary button background (pink)
BG_BUTTON_HOVER = "#FFB3B3"     # Primary button hover state
BG_SELECTED     = "#FF8080"     # Selected / active toggle state
BG_DANGER       = "#ff6666"     # Destructive / confirm-danger button
BG_DANGER_HOVER = "#ff3333"     # Destructive button hover
BG_DISABLED     = "#e0e0e0"     # Disabled button background
BG_HOME_BUTTON  = "#E6EEF3"     # Home / neutral button background

# Text colours
TEXT_PRIMARY    = "#333333"     # Default body / heading text
TEXT_SECONDARY  = "#555555"     # Subdued labels, captions
TEXT_DISABLED   = "#888888"     # Disabled button text
TEXT_ON_BUTTON  = "#000000"     # Text on pink buttons
TEXT_HOME       = "#2C3E50"     # Home button text

# Semantic colours
COLOR_CORRECT   = "#2a9d2a"     # Correct-answer green
COLOR_WRONG     = "#cc2222"     # Wrong-answer red

# Border colours
BORDER_COLOR    = "#333333"     # Standard border colour
BORDER_DISABLED = "#aaaaaa"     # Disabled border
BORDER_HOME     = "#6BAED6"     # Home button dashed border


# ── Typography (pixel sizes) ─────────────────────────────────────────────────

FONT_TITLE      = 64           # Page titles
FONT_SUBTITLE   = 48           # Section headings, large buttons
FONT_HEADING    = 40           # Prompts, sub-headings
FONT_BODY       = 36           # Question text, answer feedback
FONT_LABEL      = 32           # Counter labels, score labels, exercise buttons
FONT_BUTTON     = 28           # Dialog buttons, answer option buttons
FONT_CAPTION    = 24           # Dev page labels, table headers
FONT_TABLE      = 22           # Table body text


# ── Radii & spacing ──────────────────────────────────────────────────────────

RADIUS_LG       = 20           # Buttons, cards
RADIUS_MD       = 16           # Dialog buttons
RADIUS_SM       = 12           # Small elements, dev button

BORDER_WIDTH    = 3            # Standard border width
BORDER_WIDTH_SM = 2            # Subtle borders (home button, tables)
