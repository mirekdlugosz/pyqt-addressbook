from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QHeaderView

from addressbook.constants import BASE_UI_PATH


class AddressBookMainWindow(QMainWindow):
    def __init__(self, contact_list_model):
        super().__init__()
        ui_file = BASE_UI_PATH / "main_window.ui"
        uic.loadUi(ui_file, self)
        self._model = contact_list_model
        self.contact_list_view.setModel(contact_list_model)
        self.contact_list_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for col_index in range(contact_list_model.columnCount()):
            hide_column = not contact_list_model.is_column_visible(col_index)
            self.contact_list_view.setColumnHidden(col_index, hide_column)

        self.searchbox.textChanged.connect(self._model.set_lookup_value)
        # zdarzenia obsługiwane przez widok bezpośrednio
        self.contact_list_view.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.delete_contact_button.clicked.connect(self.delete_contact)

    def selectionChanged(self, selected, deselected):
        enable_state = bool(selected.indexes())
        self.edit_contact_button.setEnabled(enable_state)
        self.delete_contact_button.setEnabled(enable_state)

    def delete_contact(self):
        selection = self.contact_list_view.selectionModel()
        self._model.delete_contacts(selection.selectedRows())
