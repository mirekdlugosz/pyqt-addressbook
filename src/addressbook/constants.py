from pathlib import Path

from PyQt5.QtCore import Qt

BASE_UI_PATH = (Path(__file__) / "../ui/").resolve()

GENDER_LIST = [
    "Mężczyzna",
    "Kobieta",
    "Inna",
    "Brak / nie dotyczy",
    "Nieznana"
]

DEFAULT_GENDER = GENDER_LIST[-1]

QtColumnDisplayedRole = Qt.UserRole + 1
