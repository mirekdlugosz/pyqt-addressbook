from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QSortFilterProxyModel
import yaml

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

    def is_column_visible(self, index):
        column_name = ContactModel.field_name(index)
        return column_name not in self.hidden_columns

    def contact_by_index(self, index):
        try:
            return self.contact_list[index]
        except IndexError:
            return None

    def data(self, index, role):
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        contact = self.contact_by_index(index.row())
        text = contact.data(index, role)
        return text

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        elem = self.contact_list[index.row()]
        elem.setData(index, value, role)
        return True

    def rowCount(self, index=None):
        return len(self.contact_list)

    def columnCount(self, index=None):
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

        self.layoutAboutToBeChanged.emit()
        self.beginInsertRows(self.index(0, 0), index, index)

        self.contact_list.append(contact)

        self.endInsertRows()
        self.layoutChanged.emit()
        # save_data() wywołuje kontroler przy powrocie z okna edycji

    def delete_contacts(self, indexes):
        list_indexes = sorted([index.row() for index in indexes])

        self.layoutAboutToBeChanged.emit()
        self.beginRemoveRows(self.index(0, 0), list_indexes[0], list_indexes[-1])

        for index in reversed(list_indexes):
            self.contact_list.pop(index)

        self.endRemoveRows()
        self.layoutChanged.emit()
        self.save_data()

    def save_data(self):
        data = [contact.__dict__ for contact in self.contact_list]
        with open(self.data_file, 'w') as fh:
            yaml.dump(data, fh, allow_unicode=True)


class FilteredContactListModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lookup_value = None

    def set_lookup_value(self, value):
        value = value or None
        self.lookup_value = value
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if self.lookup_value is None:
            return True

        contact = self.sourceModel().contact_by_index(source_row)
        for value in contact.__dict__.values():
            if self.lookup_value in str(value):
                return True
        return False

    def is_column_visible(self, index):
        return self.sourceModel().is_column_visible(index)

    def contact_by_index(self, index):
        return self.sourceModel().contact_by_index(index)

    def new_contact(self):
        return self.sourceModel().new_contact()

    def delete_contacts(self, indexes):
        source_indexes = [self.mapToSource(index) for index in indexes]
        return self.sourceModel().delete_contacts(source_indexes)

    def save_data(self):
        self.invalidateFilter()
        return self.sourceModel().save_data()
