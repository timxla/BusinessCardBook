import logging
import sys
from typing import List
from tabulate import tabulate
import psycopg2 as pg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Create the database
engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432/namecard')
base = declarative_base()

class Namecard(base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    company = Column(String)
    email = Column(String)
    phone_num = Column(String)

base.metadata.create_all(engine)


class DataManager:

    def __init__(self):
        Session = sessionmaker(engine)
        self.session = Session()
        self.reciever = Reciever()
        self.cards = self.session.query(Namecard)
    
    def insertCard(self):
        new_entry = Namecard(name = self.reciever.recieveName(),
                            company = self.reciever.recieveCompanyName(),
                            email = self.reciever.recieveEmail(),
                            phone_num = self.reciever.recievePhoneNum())
        self.session.add(new_entry)
        self.session.commit()

    def listCards(self):
        data_buffer = []
        for card in self.cards:
            data_buffer.append([card.id, card.name, card.company, card.email, card.phone_num])
        print("\n")
        print(tabulate(data_buffer, headers=["ID", "name", "company", "email", "phone number"]))

    def selectCardID(self):
        id = int(input("\nWhich row would you like to update? Enter ID :"))        
        return id

    def selectField(self):
        field = str(input("\nEnter field that you would like to update?\n(name, company, email, phone_num) :"))
        return field

    def deleteCard(self):
        self.cards.filter(Namecard.id == self.selectCardID()).delete()

    def editCard(self):
        x = self.cards.get(self.selectCardID())
        field = self.selectField()
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

    def terminate(self):
        self.session.close()
        engine.dispose()
        logging.info("program terminated.")

          
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
    
    dm = DataManager()

    while True:
        print("\nEnter Command")
        print("___________________________________\n")
        print(command_info)
        print("___________________________________")
        command = str(input("")).upper()
        # recieve user command
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
