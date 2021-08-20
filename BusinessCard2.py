import logging
import sys
from dataclasses import dataclass
from typing import List

""" Dataclass for storing individual cards. """
""" Classmethod recieves parameters via external functions for user input """
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

""" Methods for recieving user input """
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

""" Cardbook class stores instances of BusinessCard in a list """
""" Contains various manipulation methods """
class CardBook():

    def __init__(self):
        self.cardbook: List[BusinessCard] = []

    def readFile(self):
        with open("cardbook.txt", 'r') as f:
            data = f.readlines()
        for line in data:
            if (line == '\n'):
                continue
            txt_to_card = BusinessCard(*line.split("|"))
            self.cardbook.append(txt_to_card)

    def writeFile(self):
        with open("cardbook.txt", 'w') as f:
            for entry in self.cardbook:
                f.write(str(entry))

    def addCard(self):
        new_entry = BusinessCard.recieveInput()
        self.cardbook.append(new_entry) 
        logging.info("New business card added!\n")

    def listCard(self):
        for entry in self.cardbook:
            print(str(entry), end='')

    def removeCard(self, category):
        if (category == 1):
            print("Search by company selected!")
            target_name = str(input("Enter the name of the company: "))
        
        elif (category == 2):
            print("Search by name selected!")
            target_name = str(input("Enter the name of the representative: "))

        for i in self.cardbook:
            if i.name == target_name:
                index = self.cardbook.index(i)
                break
        del self.cardbook[index]
            
    def wipeAll(self):
        self.cardbook.clear()
                                

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
                    "   - Save : save entries to a file \n"
                    "   - Quit : Exit program \n")
 
    card_book = CardBook() 
    card_book.readFile() # Reads txt file data to list for stuff

    while True:
        print("\nEnter Command")
        print("___________________________________\n")
        print(command_info)
        print("___________________________________")
        # recieve user command
        command = str(input("")).upper()
        if (command == "INSERT"):
            print("Insert selected!\n")
            card_book.addCard()

        elif (command == "LIST"):
            print("Listing all entries : \n")
            card_book.listCard()

        elif (command == "REMOVE"):
            card_book.listCard()
            print("\nSearch by: Company(1) or Name(2)\n")
            try:
                category = int(input("Menu 1 or 2?: "))
            except ValueError:
                logging.warning("Enter numbers only.")
            card_book.removeCard(category)

        elif (command == "WIPE"):
            card_book.wipeAll()
            print("All entries deleted.\n")

        elif (command == "SAVE"):
            card_book.writeFile()
            logging.info("Cardbook updated!")

        elif (command == "QUIT"):
            ans = str(input("Would you like to save your changes? (y/n)"))
            if (ans == 'y'):
                card_book.writeFile()     
                logging.info("Cardbook updated!")
            print("Program Terminated.")
            break

        else:
            logging.warning("Invalid command.")
            continue
        
if __name__ == '__main__':
    main()

