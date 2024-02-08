import pickle
from collections import UserDict
from datetime import date, datetime
from dz_11_fin import Field, Name, Phone, Birthday, Record, AddressBook


address_book = AddressBook()

def save_address_book(filename):
    with open(filename, 'wb') as file:
        pickle.dump(address_book, file)


def load_address_book(filename):
    global address_book
    try:
        with open(filename, 'rb') as file:
            address_book = pickle.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found")
        address_book = AddressBook()
    except EOFError:
        print(f"Address book from file {filename} is empty")
        address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Incorrect phone number"
        except IndexError:
            return "Give me name and phone please"
    return wrapper


#команда "add name {name}"
@input_error
def add_contact(user_input):
    new_name = user_input.split(" ", 2)[2]

    name_field = Name(new_name)
    record = Record(name_field)
    address_book.add_record(record)
    return f"Contact {new_name} added"


#команда "add phone {name} {phone}"
@input_error
def add_new_phone(user_input):
    exist_name, new_phone = user_input.split(" ", 2)[2].rsplit(" ", 1)
    found_contact = False
    for k, v in address_book.data.items():
        if k.value == exist_name:
            found_contact = True
            v.add_phone(new_phone)
            return f"Phone {new_phone} added to {exist_name}"
    
    if not found_contact:
        return f"Contact {exist_name} not found"


#команда "change {name} {old_phone} {new_phone}"
@input_error
def change_phone(user_input):
    exist_name, old_phone, new_phone = user_input.split(" ", 1)[1].rsplit(" ", 2)
    found_contact = False
    phone_changed = False
    
    for k, v in address_book.data.items():
        if k.value == exist_name:
            found_contact = True
            for p in v.phones:
                if p.value == old_phone:
                    p.value = new_phone
                    phone_changed = True
                    break
            break

    if not found_contact:
        return f"Contact {exist_name} not found"
    elif not phone_changed:
        return f"Phone number {old_phone} not found for {exist_name}"
    else:
        return f"Phone number was changed for {exist_name}"


#команда "phone {name}"
@input_error
def show_phone(user_input):
    exist_name = user_input.split(" ", 1)[1]
    for k, v in address_book.data.items():
        if k.value == exist_name:
            phones = ', '.join(phone.value for phone in v.phones)
            return f"{k.value}: {phones}"
    return f"Contact {exist_name} not found"


#команда "add birthday {name} {DD.MM.YYYY}"
@input_error
def add_birthday(user_input):
    exist_name, birthday_date = user_input.split(" ", 2)[2].rsplit(" ", 1)
    for k, v in address_book.data.items():
        if k.value == exist_name:
            v.birthday = Birthday(birthday_date)
            return f"{birthday_date} added to {exist_name}"
    return f"Contact {exist_name} not found"


#команда "birthday {name}"
@input_error
def func_days_to_birthday(user_input):
    exist_name = user_input.split(" ", 1)[1]
    for k, v in address_book.data.items():
        if k.value == exist_name:
            return f"{exist_name}, days to birthday: {v.days_to_birthday()}"
    return f"Contact {exist_name} not found"


#команда "search {search_query}"
def search_contacts(user_input):
    search_query = user_input.split(" ", 1)[1]
    result_list = []
    for k, v in address_book.data.items():
        if search_query.lower() in k.value.lower():
            result_list.append(v)
            continue

        for p in v.phones:
            if search_query in p.value:
                result_list.append(v)
                break
    
    if not result_list:
        return "No contacts found matching the search query"
    
    result = ""
    for i in result_list:
        result += f"Contact name: {i.name.value}, phones: {'; '.join(p.value for p in i.phones)}, days to birthday: {i.days_to_birthday()}\n"

    return result


#команда "show all"
def show_all():
    if not address_book.data:
        return "Address book is empty"
    result = ""
    for k, v in address_book.data.items():
        result += f"Contact name: {v.name.value}, phones: {'; '.join(p.value for p in v.phones)}, days to birthday: {v.days_to_birthday()}\n"
    return result


#команда "paginate {number_of_records}"
def pagination(user_input):
    if not address_book.data:
        return "Address book is empty"
    
    number_of_records = user_input.split(" ", 1)[1]
    result = ""
    for group in address_book.iterator(int(number_of_records)):
        for v in group:
            result += f"Contact name: {v.name.value}, phones: {'; '.join(p.value for p in v.phones)}, days to birthday: {v.days_to_birthday()}\n"
        result += "----- End of page -----\n"
    return result


#команда "delete {name}"
@input_error
def delete_contact(user_input):
    exist_name = user_input.split(" ", 1)[1]
    to_delete = None
    for k, v in address_book.data.items():
        if k.value == exist_name:
            to_delete = k
            break

    if to_delete:
        del address_book.data[to_delete]
        return f"Contact {exist_name} deleted successfully."
    else:
        return f"Contact {exist_name} not found"



def main():
    load_address_book("address_book_3.bin")
    while True:
        user_input = (input("Enter some command please: "))
        user_input_lower = user_input.lower()

        if user_input_lower == "hello":
            print("How can I help you?")

        elif user_input_lower.startswith("add name"):   #команда "add name {name}"
            print(add_contact(user_input))

        elif user_input_lower.startswith("add phone"):   #команда "add phone {name} {phone}"
            print(add_new_phone(user_input))

        elif user_input_lower.startswith("change"):   #команда "change {name} {old_phone} {new_phone}"
            print(change_phone(user_input))

        elif user_input_lower.startswith("phone"):   #команда "phone {name}"
            print(show_phone(user_input))

        elif user_input_lower.startswith("add birthday"):   #команда "add birthday {name} {DD.MM.YYYY}"
            print(add_birthday(user_input))

        elif user_input_lower.startswith("birthday"):   #команда "birthday {name}"
            print(func_days_to_birthday(user_input))

        elif user_input_lower.startswith("search"):   #команда "search {search_query}"
            print(search_contacts(user_input))

        elif user_input_lower == "show all":   #команда "show all"
            print(show_all())

        elif user_input_lower.startswith("paginate"):   #команда "paginate {number_of_records}"
            print(pagination(user_input))

        elif user_input_lower.startswith("delete"):   #команда "delete {name}"
            print(delete_contact(user_input))

        elif user_input_lower in ["good bye", "close", "exit"]:
            save_address_book("address_book_3.bin")
            print("Good bye!")
            break

        else:
            print("Invalid command")


if __name__ == '__main__':
    main()