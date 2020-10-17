from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QSize
import yaml

from addressbook.constants import QtColumnDisplayedRole
from addressbook.models.contact import ContactModel


class ContactListModel(QAbstractTableModel):
    def __init__(self, *args, data_file=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_file = data_file
        self.contact_list = self._read_contacts()
        self.hidden_columns = ("street", "building", "apartment", "zip")

    def _read_contacts(self):
        try:
            with open(self.data_file) as fh:
                contact_list = yaml.load(fh, Loader=yaml.Loader)
        except OSError:
            contact_list = []
        contact_list = [ContactModel(**data) for data in contact_list]
        return contact_list

    def _display_column(self, index):
        column_name = ContactModel.field_name(index)
        return column_name not in self.hidden_columns

    def data(self, index, role):
        if role == QtColumnDisplayedRole:
            return self._display_column(index.column())
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        contact = self.contact_list[index.row()]
        if index.column() == -1:
            return contact
        text = contact.data(index, role)
        return text

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        elem = self.contact_list[index.row()]
        elem.setData(index, value, role)
        return True

    def rowCount(self, index):
        return len(self.contact_list)

    def columnCount(self, index):
        return len(ContactModel.field_names())

    def headerData(self, section, orientation, role):
        if orientation != Qt.Horizontal:
            return None
        if role == Qt.SizeHintRole:
            return QSize(10, 30)
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.DisplayRole:
            return ContactModel.field_label(section)

    def new_contact(self):
        contact = ContactModel()
        index = len(self.contact_list)
        self.beginInsertRows(self.createIndex(0, 0), index, index + 1)
        self.contact_list.append(contact)
        self.endInsertRows()
        self.layoutChanged.emit()

    def delete_contacts(self, indexes):
        self.beginRemoveRows(self.createIndex(0, 0), indexes[0], indexes[-1])
        for index in sorted(indexes, reverse=True):
            self.contact_list.pop(index)
        self.endRemoveRows()
        self.layoutChanged.emit()
        self.save_data()

    def save_data(self):
        data = [contact.__dict__ for contact in self.contact_list]
        with open(self.data_file, 'w') as fh:
            yaml.dump(data, fh, allow_unicode=True)
