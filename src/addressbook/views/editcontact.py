from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDataWidgetMapper
from PyQt5.QtWidgets import QWidget

from addressbook.constants import BASE_UI_PATH
from addressbook.constants import GENDER_LIST


class EditContactWindow(QWidget):
    def __init__(self, contact_list_model, contact_index):
        super().__init__()
        ui_file = BASE_UI_PATH / "edit_contact_window.ui"
        uic.loadUi(ui_file, self)
        self.gender_editbox.addItems(GENDER_LIST)

        contact = contact_list_model.data(
            contact_list_model.createIndex(contact_index, -1), Qt.DisplayRole
        )

        mapper = QDataWidgetMapper(self)
        mapper.setModel(contact_list_model)
        for section, name in enumerate(contact.field_names()):
            mapper.addMapping(getattr(self, f"{name}_editbox"), section)
        mapper.setCurrentIndex(contact_index)
