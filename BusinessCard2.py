import logging
import sys
from dataclasses import dataclass
from typing import List
from enum import Enum, auto

@dataclass
class BusinessCard:

    company: str
    name: str
    email: str
    phone_num: str

    def __repr__(self):
        return f"{self.company}|{self.name}|{self.email}|{self.phone_num}\n"
    
    @classmethod
    def recieveInput(cls):
        return cls(
                recieveCompanyName(),
                recieveName(),
                recieveEmail(),
                recievePhoneNum()
                )
        
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

class CardBook():

    def __init__(self):
        self.cardbook: List[BusinessCard] = []
        with open("cardbook.txt", 'r') as f:
            data = f.readlines()
        for line in data:
            txt_to_card = BusinessCard(*line.split("|"))
            self.cardbook.append(txt_to_card)


    def addCard(self):
        new_entry = BusinessCard.recieveInput()
        self.cardbook.append(new_entry) 
        logging.info("New business card added!\n")

    def listCard(self):
        for entry in self.cardbook:
            print(str(entry))
                                

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    
    command_info = ("   - Insert : insert an entry \n"
                    "   - List : list all entries \n"
                    "   - Remove : remove an entry \n"
                    "   - Wipe : remove all entries \n"
                    "   - Quit : Exit program \n")
 
    card_book = CardBook() 

    while True:
        print("\nEnter Command")
        print("___________________________________\n")
        print(command_info)
        print("___________________________________")
        #recieve user command
        command = str(input(""))
        if (command == "Insert"):
            print("Insert selected!\n")
            card_book.addCard()
 
        elif (command == "List"):
            print("Listing all entries : \n")
            card_book.listCard()

        elif (command == "Remove"):
            print("Search by: Company(1)\n"
                    "          Name(2)\n")
            category = int(input())
            card_book.removeCard()

        elif (command == "Quit"):
            print("Program terminated")
            break

        else:
            logging.warning("Invalid command.")
            continue
        

if __name__ == '__main__':
    main()

