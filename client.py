#Notebook application
#Distributed systems assignment2
#Santeri Ruuskanen 0567818
#04.04.21


##CLIENT SIDE##



from xmlrpc.client import ServerProxy
from datetime import date, datetime



# Defining the server address

proxy = ServerProxy('http://localhost:5000')



# Basic menu for making it easy for the client to navigate
def menu():
    print("\n1 - Create a note\n2 - List note topics\n3 - Fetch topic\n0 - Quit")
    try:
        choice = int(input())
        if (choice == 1):
            create_note()
        elif (choice == 2):
            list_topics()
        elif (choice == 3):
            find_topic()
        elif (choice == 0):
            print("Client closing...")
            exit(0)
        else:
            print("Invalid choise, try again!")
    except ValueError:
        print("Please input an integer between 0 and 3.")



#time for the timestamps in notes

def get_time():
    _date = date.today().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    timestamp = "{} - {}".format(_date, time)
    return timestamp


# Takes the data for the new note and sends them to the server

def create_note():

    print("Enter the data")

    topic = input("TOPIC: ")

    title = input("TITLE: ")

    text = input("TEXT: ")

    #form an array that consists of input data and send it to server function (create_topic)
    note = [topic, title, text, get_time()]
    if proxy.create_topic(note) == False:
        print("Failed to create a note.")
        return

    print("\nSuccesfully created a note on topic '{}'!".format(topic))


#Finds and prints already existing topic and its title, text and timestamp

def find_topic():
    topic = input("Enter a topic to search: ")

    notelist = proxy.find_topic(topic)

    if not notelist:
        print("Couldn't find topics on '{}'".format(topic))
        return

    elif notelist[0] == 'error':
        print("Serverside error occurred")
        return

    print("\n")
    print("Notes made on topic '{}':".format(topic))

    for n in notelist:
        print("\nNote: {}\nText: {}\nTime: {}".format(n[0],n[1],n[2]))



#Fetching all the notes from the server

def list_topics():
    print("\nFetching the topics...")
    try:
        topics = proxy.get_topics()
        if not topics:
            print("\nThe notebook is currently empty. Create some notes and try again.\n")
            return
        print("\nList of topics in notebook:\n")
    except:
        print("Error while fetching a list of topics.")
        return
    for t in topics:
        print(t)



# When the program starts menu -function starts running immidiately.

if __name__ == '__main__':
    print("NOTEBOOK")
    while(True):
        menu()