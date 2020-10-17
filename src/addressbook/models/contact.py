from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractListModel

from addressbook.constants import DEFAULT_GENDER


class ContactModel(QAbstractListModel):
    _FIELDS = {
        "first_name": "Imię",
        "last_name": "Nazwisko",
        "age": "Wiek",
        "gender": "Płeć",
        "street": "Ulica",
        "building": "Nr budynku",
        "apartment": "Nr mieszkania",
        "city": "Miasto",
        "zip": "Kod pocztowy",
    }

    _DEFAULT_VALUES = {
        "age": 0,
        "gender": DEFAULT_GENDER
    }

    def __init__(self, *args, **kwargs):
        for field_name in self._FIELDS:
            value = kwargs.pop(field_name, None)
            if value is None and field_name in self._DEFAULT_VALUES:
                value = self._DEFAULT_VALUES[field_name]
            setattr(self, field_name, value)
        super().__init__(*args, **kwargs)

    def data(self, index, role):
        values_list = list(self.__dict__.values())
        return values_list[index.column()]

    def setData(self, index, value, role):
        setattr(self, self.field_name(index.column()), value)
        return True

    def rowCount(self, index):
        return len(self.__dict__)

    @classmethod
    def field_names(cls):
        return list(cls._FIELDS.keys())

    @classmethod
    def field_labels(cls):
        return list(cls._FIELDS.values())

    @classmethod
    def field_name(cls, index):
        names = cls.field_names()
        return names[index]

    @classmethod
    def field_label(cls, index):
        labels = cls.field_labels()
        return labels[index]

    def __repr__(self):
        return "<{first_name} {last_name} {age}>".format(**self.__dict__)
