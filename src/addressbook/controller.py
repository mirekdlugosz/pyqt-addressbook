from addressbook.views import AddressBookMainWindow
from addressbook.views import EditContactWindow


class AddressBookController:
    def __init__(self, app, contact_list_model):
        self._app = app
        self._contact_list = contact_list_model
        self._addressbook_widget = None
        self.main_window = AddressBookMainWindow(contact_list_model=self._contact_list)

        # zdarzenia wymieniające widok - w kontrolerze, aby widoki nie musiały
        # o sobie wiedzieć
        self.main_window.new_contact_button.clicked.connect(self.open_new_contact_view)
        self.main_window.edit_contact_button.clicked.connect(self.open_edit_contact_view)

        # mógłby to robić widok, ale nie ma referencji do `app`
        self.main_window.quit_button.clicked.connect(self._app.exit)

        self.main_window.show()

    def open_new_contact_view(self):
        self._contact_list.new_contact()
        model_index = self._contact_list.rowCount() - 1
        self._create_edit_contact_view(model_index)

    def open_edit_contact_view(self):
        selection = self.main_window.contact_list_view.selectionModel()
        model_index = selection.selectedIndexes()[0].row()
        self._create_edit_contact_view(model_index)

    def _create_edit_contact_view(self, contact_index):
        edit_window = EditContactWindow(
            contact_list_model=self._contact_list, contact_index=contact_index
        )
        self._addressbook_widget = self.main_window.takeCentralWidget()
        self.main_window.setCentralWidget(edit_window)
        edit_window.back_button.clicked.connect(self.close_edit_contact_view)

    def close_edit_contact_view(self):
        self.main_window.setCentralWidget(self._addressbook_widget)
        self._addressbook_widget = None
        self._contact_list.save_data()
