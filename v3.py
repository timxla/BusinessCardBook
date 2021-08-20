import logging
import sys
from dataclasses import dataclass
from typing import List
from tabulate import tabulate
import psycopg2 as pg2

@dataclass
class BusinessCard:

    company: str
    name: str
    email: str
    phone_num: str

    @classmethod
    def recieveInput(cls):
        return cls(
                recieveCompanyName(),
                recieveName(),
                recieveEmail(),
                recievePhoneNum()
                )

    def returnInsertQuery(self):
        return f"INSERT INTO book VALUES (default,'{self.company}', '{self.name}', '{self.email}', '{self.phone_num}');"

    
""" -----------Methods for recieving user input------------- """
def recieveCompanyName():
    while True:
        try:
            company = str(input("Enter company name : "))
        except ValueError:
            logging.warning("Only string input available!")
            continue
        else:
            return company

def recieveName():
    while True:
        try:
            name = str(input("Enter representative's name : "))
        except ValueError:
            logging.waring("Only string input available!")
            continue
        else:
            return name

def recieveEmail():
    while True:
        email = str(input("Enter representative's email : "))
        if(email.find(".") == -1 or email.find("@") == -1):
            logging.warning("Email has to be in form __@___.__")
            continue
        elif(email.rfind(".") < email.rfind("@")):
            logging.warning("Email has to be in form __@___.__")
        else:
            return email

def recievePhoneNum():
    while True:
        try:
            phone = str(input("Enter representative's phone number (numbers only) : "))
        except ValueError:
            logging.warning("Only numbers available!")
            continue
        else:
            return phone 
"""---------------------------------------------------------- """

class Database:

    def __init__(self):
        
        self.db = pg2.connect(
                host = "localhost",
                dbname = "namecard",
                user = "postgres",
                password = "1234",
                port =5432)

        self.cur = self.db.cursor()

    def closeDatabase(self):
        self.cur.close()
        self.db.close()
    
    def printCards(self):
        self.cur.execute(f"SELECT * FROM book")
        tables = self.cur.fetchall()
        list_tables = []
        for i in tables:
            list_tables.append(list(i))
        print(tabulate(list_tables, headers=["ID", "company", "name", "email", "Phone Number"]))

    def addCard(self, card):
        self.cur.execute(card.returnInsertQuery())
        self.db.commit()

    def deleteCard(self, ID):
        self.cur.execute(f"DELETE FROM book WHERE id = '{ID}';")
        self.db.commit()

    def updateCard(self, row, column, new_info):
        self.cur.execute(f"UPDATE book SET {column} = '{new_info}' WHERE id = '{row}';")
        self.db.commit()

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    command_info = ("   - Insert : insert an entry \n"
                    "   - List : list all entries \n"
                    "   - Delete : remove an entry \n"
                    "   - Edit : remove all entries \n"
                    "   - Quit : Exit program \n")
 
    card_book = Database()

    while True:
        print("\nEnter Command")
        print("___________________________________\n")
        print(command_info)
        print("___________________________________")
        # recieve user command
        command = str(input("")).upper()
        if (command == "INSERT"):
            card = BusinessCard.recieveInput()
            card_book.addCard(card)

        elif (command == "LIST"):
            print("Listing all entries : \n")
            card_book.printCards()

        elif (command == "DELETE"):
            print("Listing all entries : \n")
            card_book.printCards()
            row = int(input("Enter row number for removal : "))
            card_book.deleteCard(row)
            logging.info(f"Entry row number {row} deleted.")

        elif (command == "EDIT"):
            print("Listing all entries : \n")
            card_book.printCards()
            row = int(input("Enter row number for edit : "))
            column = str(input("Enter column name for edit (company, name, email, phone) : "))
            new_info = str(input("Enter info : "))
            card_book.updateCard(row, column, new_info)
            

        elif (command == "QUIT"):
            card_book.closeDatabase()
            print("Program Terminated.")
            break

        else:
            logging.warning("Invalid command.")
            continue
        
if __name__ == '__main__':
    main()
