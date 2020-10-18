from pathlib import Path

BASE_UI_PATH = (Path(__file__) / "../ui/").resolve()

GENDER_LIST = [
    "Mężczyzna",
    "Kobieta",
    "Inna",
    "Brak / nie dotyczy",
    "Nieznana"
]

DEFAULT_GENDER = GENDER_LIST[-1]
