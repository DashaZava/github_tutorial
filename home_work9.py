def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Invalid input. Please try again."
    return wrapper


contacts = {}


@input_error
def add_contact(name, phone):
    contacts[name] = phone
    return f"Contact {name} with phone number {phone} added."


@input_error
def change_contact(name, phone):
    if name in contacts:
        contacts[name] = phone
        return f"Phone number for contact {name} changed to {phone}."
    else:
        return f"Contact {name} not found."


@input_error
def get_phone(name):
    if name in contacts:
        return f"Phone number for contact {name}: {contacts[name]}"
    else:
        return f"Contact {name} not found."


def show_all_contacts():
    if contacts:
        return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
    else:
        return "No contacts found."


def main():
    while True:
        command = input("Enter a command: ").lower()

        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone = command.split()
            result = add_contact(name, phone)
            print(result)
        elif command.startswith("change"):
            _, name, phone = command.split()
            result = change_contact(name, phone)
            print(result)
        elif command.startswith("phone"):
            _, name = command.split()
            result = get_phone(name)
            print(result)
        elif command == "show all":
            result = show_all_contacts()
            print(result)
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
