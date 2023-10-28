from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format. Please provide 10 digits.")
        self.value = value


    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    def __init__(self, value):
        if not self.validate_birthday(value):
            raise ValueError("Invalid birthday format. Please provide DD.MM.YYYY.")
        self.value = value


    @staticmethod
    def validate_birthday(birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self, phone):
        self.phones.append(Phone(phone))


    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]


    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return str(p)
        return None


    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


    def __str__(self):
        phones_str = "; ".join(str(phone) for phone in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "No birthday"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"


    def get_phones(self):
        return [str(phone) for phone in self.phones]


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


    def find(self, name):
        return self.data.get(name)


    def delete(self, name):
        if name in self.data:
            del self.data[name]


    def get_all_records(self):
        return list(self.data.values())


    def get_birthdays_per_week(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.get_all_records():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").replace(year=today.year)
                if today <= birthday_date <= next_week:
                    upcoming_birthdays.append(f"{record.name.value}: {birthday_date.strftime('%d.%m')}")
        
        return upcoming_birthdays


def parse_input(user_input):
    cmd, *args = user_input.strip().lower().split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter a valid name."
        except IndexError:
            return "Command requires more arguments."
    return inner


@input_error
def add_contact(args, book):
    if len(args) < 2:
        return "Give me name and phone please."
    
    name, phone = args
    if len(phone) != 10:
        return "Phone number must be 10 digits."
    
    result = book.find(name)
    if result:
        return "Contact already exists."
    else:
        book.add_record(Record(name))
        book[name].add_phone(phone)
        return "Contact added."


@input_error
def change_contact(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    
    name, new_phone = args
    if len(new_phone) != 10:
        raise ValueError("Phone number must be 10 digits.")
    
    contact = book.find(name)
    if contact:
        contact.remove_phone(contact.get_phones()[0])  # Remove the old phone
        contact.add_phone(new_phone)  # Add the new phone
        return "Contact updated."
    else:
        raise ValueError("Contact not found.")


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return "; ".join(record.get_phones())
    else:
        raise KeyError


def show_all(book):
    records = book.get_all_records()
    if records:
        return "\n".join(str(record) for record in records)
    else:
        return "Address book is empty."


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return ValueError("Give me name and date of birth please.")
    
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError("Contact not found.")


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return f"Birthday: {record.birthday.value}"
        else:
            return "No birthday set for this contact."
    else:
        raise KeyError


def birthdays(book):
    upcoming_birthdays = book.get_birthdays_per_week()
    if upcoming_birthdays:
        return "Upcoming birthdays:\n" + "\n".join(upcoming_birthdays)
    else:
        return "No upcoming birthdays in the next week."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
    