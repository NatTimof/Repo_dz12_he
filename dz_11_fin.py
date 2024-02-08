from collections import UserDict
from datetime import date, datetime

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def validate(self, value):
        pass

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.validate(value)
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def validate(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Invalid phone number format")


class Birthday(Field):
    def validate(self, value):
        if value is not None:
            try:
                date_of_birth_dt = datetime.strptime(value, '%d.%m.%Y').date()
            except:
                print("Invalid date format, should be DD.MM.YYYY")


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

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
            else:
                raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def days_to_birthday(self):
        if self.birthday.value:
            today = date.today()
            date_of_birth_datetime = datetime.strptime(self.birthday.value, '%d.%m.%Y').date()
            birthday_current_year = date_of_birth_datetime.replace(year=today.year)

            if today > birthday_current_year:
                birthday_next_year = date_of_birth_datetime.replace(year=today.year + 1)
                days_to_bd = (birthday_next_year - today).days

            elif today <= birthday_current_year:
                days_to_bd = (birthday_current_year - today).days

            return days_to_bd
        return ""

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, days to birthday: {self.days_to_birthday()}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name, None)

    def iterator(self, number_of_records):
        records = list(self.data.values())
        for i in range(0, len(records), number_of_records):
            yield records[i:i + number_of_records]


