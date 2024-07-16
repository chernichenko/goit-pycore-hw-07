from datetime import datetime, timedelta

class Birthday:
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')

class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def add_phone(self, phone: str):
        self.phones.append(phone)

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, record: Record):
        self.contacts.append(record)

    def remove_contact(self, name: str):
        for contact in self.contacts:
            if contact.name == name:
                self.contacts.remove(contact)
                break

    def find_contact(self, name: str) -> Record:
        for contact in self.contacts:
            if contact.name == name:
                return contact
        return None

    def get_upcoming_birthdays(self) -> list:
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for contact in self.contacts:
            if contact.birthday and contact.birthday.date.month == next_week.month:
                if contact.birthday.date.day >= today.day and contact.birthday.date.day <= next_week.day:
                    upcoming_birthdays.append(contact)
        return upcoming_birthdays

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return wrapper

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_str, *_ = args
    record = book.find_contact(name)
    if record:
        birthday = Birthday(birthday_str)
        record.add_birthday(birthday)
        return f"Birthday added for {name}: {birthday}"
    else:
        return f"Contact '{name}' not found."

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find_contact(name)
    if record and record.birthday:
        return f"Birthday of {name}: {record.birthday}"
    elif record and not record.birthday:
        return f"No birthday found for {name}."
    else:
        return f"Contact '{name}' not found."

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{contact.name} - {contact.birthday}" for contact in upcoming_birthdays])
    else:
        return "No upcoming birthdays."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find_contact(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_contact(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find_contact(name)
    if record:
        if old_phone in record.phones:
            record.phones.remove(old_phone)
            record.phones.append(new_phone)
            return f"Phone number updated for {name}."
        else:
            return f"No phone number '{old_phone}' found for {name}."
    else:
        return f"Contact '{name}' not found."

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find_contact(name)
    if record:
        return f"Phones of {name}: {', '.join(record.phones)}"
    else:
        return f"Contact '{name}' not found."

@input_error
def show_all(book: AddressBook):
    if book.contacts:
        return "\n".join([f"{contact.name}: {', '.join(contact.phones)}" for contact in book.contacts])
    else:
        return "No contacts in the address book."

if __name__ == "__main__":
    main()
