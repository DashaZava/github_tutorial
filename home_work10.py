from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def __str__(self):
        phones_str = ', '.join([str(phone) for phone in self.phones])
        return f"Name: {self.name}, Phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search_records(self, search_term):
        results = []
        for name, record in self.data.items():
            if search_term.lower() in name.lower():
                results.append(record)
        return results


def main():
    address_book = AddressBook()

    while True:
        command = input("Enter a command: ").lower()

        if command == "add":
            name = input("Enter name: ")
            record = Record(name)
            address_book.add_record(record)
            phone = input("Enter phone: ")
            record.add_phone(phone)
        elif command == "search":
            search_term = input("Enter search term: ")
            results = address_book.search_records(search_term)
            if results:
                for record in results:
                    print(record)
            else:
                print("No records found.")
        elif command == "exit":
            print("Good bye!")
            break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
