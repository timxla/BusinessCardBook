# Namecard Manager with PostgreSQL and SQLAlchemy

import logging
import sys
from typing import List
from tabulate import tabulate
import psycopg2 as pg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the engine
engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432/namecard')
base = declarative_base()

# Namecard class (SQLAlchemy)
class Namecard(base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    company = Column(String)
    email = Column(String)
    phone_num = Column(String)

# Sync metadata
base.metadata.create_all(engine)


# Datamanager class:
# Create session, make a reciever instance (for input)
# Query from session and save to self.cards beforehand (If table is large, query per action)
class DataManager:

    def __init__(self):
        Session = sessionmaker(engine)
        self.session = Session()
        self.reciever = Reciever()
    
    # Add a card with data obtained from reciever
    def insertCard(self):
        new_entry = Namecard(name = self.reciever.recieveName(),
                            company = self.reciever.recieveCompanyName(),
                            email = self.reciever.recieveEmail(),
                            phone_num = self.reciever.recievePhoneNum())
        self.session.add(new_entry)
        self.session.commit()

    def queryAll(self):
        return self.session.query(Namecard).all()

    def queryByPage(self, offset, limit):
        return self.session.query(Namecard).offset(offset).limit(limit).all()

    def queryDBSize(self):
        return self.session.query(Namecard).count()

    # List all cards
    def listCards(self):
        # Implememnt Paging
        data_buffer = []
        number_of_pages = int(self.queryDBSize()/5 + 1)  
        for i in range(number_of_pages):
            page = self.queryByPage(i*5, 5)
            for card in page:
                data_buffer.append([card.id, card.name, card.company, card.email, card.phone_num])
            print("\n")
            print("Page " + str(i) + "\n")
            print(tabulate(data_buffer, headers=["ID", "name", "company", "email", "phone number"]))
            if i == number_of_pages - 1:
                return
            else:
                print("See next page? \n")
                if(self.reciever.userAnswer() == "Y"):
                    data_buffer.clear()
                    continue
                else:
                    data_buffer.clear()
                    break

    # Delete card
    def deleteCard(self):
        self.cards.filter(Namecard.id == self.reciever.selectCardID()).delete()

    # Edit card
    def editCard(self):
        x = self.cards.get(self.reciever.selectCardID())
        field = self.reciever.selectField()
        if (field == "name"):
            newdata = str(input("Enter new name : "))
            x.name = newdata
        elif (field == "company"):
            newdata = str(input("Enter new company : "))
            x.company = newdata
        elif (field == "email"):
            newdata = str(input("Enter new email : "))
            x.email = newdata
        elif (field == "phone_num"):
            newdata = str(input("Enter new phone number : "))
            x.phone_num = newdata

    # Close session, dispose engine and end program
    def terminate(self):
        self.session.close()
        engine.dispose()
        logging.info("program terminated.")

          
# Reciever Class
# Responisible for recieving all input and checking for exceptions
class Reciever:

    def recieveCompanyName(self):
        while True:
            try:
                company = str(input("Enter company name : "))
            except ValueError:
                logging.warning("Only string input available!")
                continue
            else:
                return company

    def recieveName(self):
        while True:
            try:
                name = str(input("Enter representative's name : "))
            except ValueError:
                logging.waring("Only string input available!")
                continue
            else:
                return name

    def recieveEmail(self):
        while True:
            email = str(input("Enter representative's email : "))
            if(email.find(".") == -1 or email.find("@") == -1):
                logging.warning("Email has to be in form __@___.__")
                continue
            elif(email.rfind(".") < email.rfind("@")):
                logging.warning("Email has to be in form __@___.__")
            else:
                return email

    def recievePhoneNum(self):
        while True:
            try:
                phone = str(input("Enter representative's phone number (numbers only) : "))
            except ValueError:
                logging.warning("Only numbers available!")
                continue
            else:
                return phone 

    # Select card ID for editing or deleting
    def selectCardID(self):
        id = int(input("\nWhich row would you like to update? Enter ID :"))        
        return id

    # Select card Field for editing or deleting
    def selectField(self):
        field = str(input("\nEnter field that you would like to update?\n(name, company, email, phone_num) :"))
        return field
    
    def userAnswer(self):
        while True:
            answer = str(input("Yes or No (Enter 'y' or 'n') : ")).upper()
            if (answer == 'Y' or answer == 'N'):
                return answer
            else:
                logging.warning("Try again!\n")
                continue
            
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
    
    # Create Datamanger instance
    dm = DataManager()

    while True:
        print("\nEnter Command")
        print("___________________________________\n")
        print(command_info)
        print("___________________________________")
        # Recieve user command, upper() for disabling case-sensitivity
        command = str(input("")).upper()
        if (command == "INSERT"):
            dm.insertCard()
            
        elif (command == "LIST"):
            dm.listCards()

        elif (command == "DELETE"):
            dm.listCards()
            dm.deleteCard()

        elif (command == "EDIT"):
            dm.listCards()
            dm.editCard()
            
        elif (command == "QUIT"):
            dm.terminate()
            exit(0);

        else:
            logging.warning("Invalid command.")
            continue
        
if __name__ == '__main__':
    main()
