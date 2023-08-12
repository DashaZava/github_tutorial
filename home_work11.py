from collections import UserDict
from datetime import datetime, timedelta


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
    def __set__(self, instance, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number")
        self.value = value


class Birthday(Field):
    def __set__(self, instance, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        self.value = value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

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

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today()
            next_birthday = datetime(today.year, int(
                self.birthday.value[5:7]), int(self.birthday.value[8:]))
            if next_birthday < today:
                next_birthday = datetime(
                    today.year + 1, int(self.birthday.value[5:7]), int(self.birthday.value[8:]))
            days_left = (next_birthday - today).days
            return days_left

    def __str__(self):
        phones_str = ', '.join([str(phone) for phone in self.phones])
        birthday_str = f", Birthday: {self.birthday}" if self.birthday.value else ""
        return f"Name: {self.name}, Phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search_records(self, search_term):
        results = []
        for name, record in self.data.items():
            if search_term.lower() in name.lower():
                results.append(record)
        return results

    def iterator(self, batch_size):
        keys = list(self.data.keys())
        num_batches = len(keys) // batch_size + (len(keys) % batch_size != 0)
        for batch_num in range(num_batches):
            start_idx = batch_num * batch_size
            end_idx = start_idx + batch_size
            batch_keys = keys[start_idx:end_idx]
            yield [self.data[key] for key in batch_keys]


def main():
    address_book = AddressBook()

    while True:
        command = input("Enter a command: ").lower()

        if command == "add":
            name = input("Enter name: ")
            birthday = input("Enter birthday (YYYY-MM-DD, optional): ")
            record = Record(name, birthday)
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
        elif command == "list":
            batch_size = int(input("Enter batch size: "))
            for batch in address_book.iterator(batch_size):
                for record in batch:
                    print(record)
                input("Press Enter to continue...")
        elif command == "exit":
            print("Good bye!")
            break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
