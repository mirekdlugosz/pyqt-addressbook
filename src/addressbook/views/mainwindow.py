from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QHeaderView

from addressbook.constants import BASE_UI_PATH
from addressbook.constants import QtColumnDisplayedRole


class AddressBookMainWindow(QMainWindow):
    def __init__(self, contact_list_model):
        super().__init__()
        ui_file = BASE_UI_PATH / "main_window.ui"
        uic.loadUi(ui_file, self)
        self._model = contact_list_model
        self.contact_list_view.setModel(contact_list_model)
        self.contact_list_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for raw_index in range(contact_list_model.columnCount(-1)):
            index = contact_list_model.createIndex(0, raw_index)
            column_visible = not contact_list_model.data(index, QtColumnDisplayedRole)
            self.contact_list_view.setColumnHidden(raw_index, column_visible)

        # zdarzenia obsługiwane przez widok bezpośrednio
        self.contact_list_view.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.delete_contact_button.clicked.connect(self.delete_contact)

    def selectionChanged(self, selected, deselected):
        enable_state = bool(selected.indexes())
        self.edit_contact_button.setEnabled(enable_state)
        self.delete_contact_button.setEnabled(enable_state)

    def delete_contact(self):
        selection = self.contact_list_view.selectionModel()
        rows_index = [index.row() for index in selection.selectedRows()]
        self._model.delete_contacts(rows_index)
