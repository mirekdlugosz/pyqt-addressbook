import argparse
import sys

from PyQt5.QtWidgets import QApplication

from addressbook.controller import AddressBookController
from addressbook.models.contact_list import ContactListModel


def process_args():
    description = "Addressbook manager"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--file", "-f", help="YAML file with contacts",
    )
    # parser.add_argument(
    #     "--debug", "-v", help="Be more verbose; may be passed up to 5 times", action="count"
    # )
    return parser.parse_known_args()


def main():
    args, unparsed_args = process_args()
    app = QApplication(unparsed_args)
    contact_list_model = ContactListModel(data_file=args.file)
    controller = AddressBookController(app, contact_list_model)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
