"""
Test program for Genesys interview.
This program allows storing Name, Phone number and birthday.
At first run it creates the file in the script's folder, where it stores the contacts
"""

import csv
from datetime import date, datetime

FILE_NAME = 'PhoneBook_db.txt'


class PhoneBook:
    def __init__(self):
        self.data = []

    def add_new_entry(self, name, phone, birthday):
        new_contact = PhoneRecord(name, phone, birthday.date())
        # add contact to the variable that stores the contacts
        self.data.append(new_contact)
        # add contact to the end of the file, so don't lose it in case of any exceptions occurred
        self.add_data_to_file(new_contact)
        print(f'New contact {name} added to the phone book\n')

    def remove_entry_by_name(self, name):
        found_flag = False
        for entry in self.data:
            if entry.name == name:
                found_flag = True
                self.data.remove(entry)
                print(f'Contact {name} deleted from phone book\n')
        if not found_flag:
            print(f'Contact with name {name} not found\n')
        else:
            with open(FILE_NAME, 'w') as file:
                file.write('Name,Phone Number,Birthday\n')
                for contact in self.data:
                    file.write(f'{contact.name},{contact.phone},{contact.bday}\n')

    def restore_data_from_file(self):
        # reading data from file in the script's folder, if file exists
        try:
            with open(FILE_NAME, 'r') as file:
                csv_reader = csv.reader(file)
                header_row = True
                for row in csv_reader:
                    # ignoring header in file
                    if header_row:
                        header_row = False
                    else:
                        self.data.append(PhoneRecord(*row))
        except FileNotFoundError:
            with open(FILE_NAME, 'w') as file:
                file.write('Name,Phone Number,Birthday\n')
                print("Phone book not found, new file has been created.\n")

    @staticmethod
    def add_data_to_file(contact):
        with open(FILE_NAME, 'a') as file:
            file.write(f'{contact.name},{contact.phone},{contact.bday}\n')

    def show_all_contacts(self):
        if len(self.data) == 0:
            print('No records in phone book\n')
        else:
            # calculating width of name column
            name_length = max(len(i.name) for i in self.data)
            phone_number_length = max(len(i.phone) for i in self.data)
            print('Name'.ljust(name_length + 1), 'Phone Number'.ljust(phone_number_length + 1), 'Birthday')
            for elem in self.data:
                print(f'{elem.name.ljust(name_length + 1)} {elem.phone.ljust(phone_number_length + 1)} {elem.bday}')
            print()

    def show_contact_info(self, name):
        found_flag = False
        for entry in self.data:
            if entry.name == name:
                found_flag = True
                print(f'Name: {entry.name}\n'
                      f'Phone number: {entry.phone}\n'
                      f'Birthday: {entry.bday}\n')
        if not found_flag:
            print(f'Contact with name {name} not found\n')

    def birthday_reminder(self):
        # When the program starts, checks if any of the contacts have a birthday today
        current_date = date.today()
        for contact in self.data:
            contact_bday = datetime.strptime(contact.bday, '%Y-%m-%d')
            if contact_bday.day == current_date.day and contact_bday.month == current_date.month:
                age = current_date.year - contact_bday.year
                print(f'{contact.name} has a birthday today! {age} years old! '
                      f'Don\'t forget to congratulate him. Here\'s the phone number: {contact.phone}\n')


class PhoneRecord:
    def __init__(self, name, phone, birthday):
        self.name = name
        self.phone = phone
        self.bday = birthday


if __name__ == "__main__":
    book = PhoneBook()
    book.restore_data_from_file()
    book.birthday_reminder()
    while True:
        choice = int(input('Select action:\n'
                           '1. Add new contact to the phone book\n'
                           '2. Remove a contact from the phone book\n'
                           '3. Show contact\'s information\n'
                           '4. Show all contacts\n'
                           '5. Exit program\n'))
        if choice == 5:
            break

        elif choice == 1:
            contact_name = input("Enter contact name: \n").title()
            contact_phone = input("Enter phone number: \n")
            contact_birthday = ""
            # check for correct birthday input
            while contact_birthday == "":
                try:
                    contact_birthday = datetime.strptime(input("Enter birthday in format dd/mm/yyyy: \n"), '%d/%m/%Y')
                except ValueError:
                    print("Please, enter correct date using format dd/mm/yyyy\n")

            book.add_new_entry(contact_name, contact_phone, contact_birthday)

        elif choice == 2:
            contact_to_remove = input("Enter contact name to remove: \n").title()
            book.remove_entry_by_name(contact_to_remove)

        elif choice == 3:
            info_name = input("Enter contact name that you want to search for: \n").title()
            book.show_contact_info(info_name)

        elif choice == 4:
            book.show_all_contacts()

        else:
            print("Choice is not correct, select number from 1 to 5.\n")
