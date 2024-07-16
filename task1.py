from datetime import datetime
from datetime import timedelta

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

    def search_contact(self, name: str) -> Record:
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

address_book = AddressBook()

contact1 = Record("John Doe")
contact1.add_birthday(Birthday("15.07.1990"))
contact1.add_phone("123456789")
contact1.add_phone("987654321")
address_book.add_contact(contact1)

contact2 = Record("Jane Smith")
contact2.add_birthday(Birthday("20.07.1985"))
contact2.add_phone("111222333")
address_book.add_contact(contact2)

search_name = "John Doe"
found_contact = address_book.search_contact(search_name)
if found_contact:
    print(f"Found contact: {found_contact.name}")
    print(f"Birthday: {found_contact.birthday}")
    print(f"Phones: {', '.join(found_contact.phones)}")
else:
    print(f"Contact '{search_name}' not found.")

upcoming_birthdays = address_book.get_upcoming_birthdays()
print("\nUpcoming birthdays:")
for contact in upcoming_birthdays:
    print(f"{contact.name} - {contact.birthday}")

