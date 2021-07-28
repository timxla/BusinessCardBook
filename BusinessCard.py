import logging
import sys

class BusinessCard:

    def __init__(self, company, name, email, phone_num):
        self.company = company
        self.name = name
        self.email = email
        self.phone_num = phone_num

    def printCard(self):
        return (self.company + " | " + self.name + " | " + self.email + " | " + self.phone_num + "\n")

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

def receiveEmail():
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

def main():
    
    command_info = ("   - Insert : insert an entry \n"
                    "   - List : list all entries \n"
                    "   - Quit : Exit program \n")


    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
            ]
    )

    book = []

    while True:
        print("Enter Command")
        print("___________________________________\n")
        print(command_info)
        print("___________________________________")
        command = str(input(""))
        if (command == "Insert"):
            print("Insert selected!\n")
            new_entry = BusinessCard(recieveCompanyName(), recieveName(), receiveEmail(), recievePhoneNum())
            with open("cardbook.txt", mode='a') as f:
                f.write(new_entry.printCard())
            book.append(new_entry) 
            logging.info("New business card added!\n")
            
        elif (command == "List"):
            #for entry in book:
                #print(entry.printCard())
            print("Listing all entries : \n")
            with open("cardbook.txt", mode='r') as f:
                info = f.readlines()
            for line in info:
                print(line.strip())
        elif (command == "Quit"):
            print("Program terminated")
            break
        else:
            logging.warning("Invalid command.")
            continue
        

if __name__ == '__main__':
    main()

