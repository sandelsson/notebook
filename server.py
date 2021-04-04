#Notebook application
#Distributed systems assignment2
#Santeri Ruuskanen 0567818
#04.04.21


##SERVER SIDE##


from xmlrpc.server import SimpleXMLRPCServer
from datetime import date, datetime
import xml.etree.ElementTree as ET
import os
import threading

#Defining xml database tree and root for data fetching

tree = ET.parse('db.xml')
root = tree.getroot()

# Defining the server
server = SimpleXMLRPCServer(('127.0.0.1', 5000), logRequests=True, allow_none=True)

#function to get the time for the server log
def get_time():
    _date = date.today().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    timestamp = "[{} - {}]".format(_date, time)
    return timestamp


#searches for topics in xml file and returns them to the client

def get_topics():
    print("Fetching topics from xml file...\t\t\t{}".format(get_time()))
    return_topics = [] 
    topics = tree.findall('topic')
    for t in topics:
        return_topics.append(t.attrib.get('name').strip())
    print("Topics returned\t\t\t{}".format(get_time()))
    return return_topics



#finding the topics from the xml file based on the clients input

def find_topic(topic):
    print("{}: Fetching topics...".format(get_time()))
    try:
        return_topics = [] #list for the matching topic
        topics = tree.findall('topic')
        for t in topics:
            if (topic == t.attrib.get('name')):
                notes = t.findall('note')
                for n in notes:
                    return_notes = [] #list for the notes under the matching topic
                    return_notes.append(n.attrib.get('name').strip())
                    return_notes.append(n.find('text').text.strip())
                    return_notes.append(n.find('timestamp').text.strip())
                    return_topics.append(return_notes)
        print("Topics fetched\t\t\t{}".format(get_time()))
        return return_topics
    except:
        print("Topic fetch error\t\t\t".format(get_time()))
        return return_topics
 

# Creating a new note
# if the topic already exists, append the existing topic
# if not --> create a new entry
# source: https://stackabuse.com/reading-and-writing-xml-files-in-python/


def create_topic(note):
    try:
        for a in tree.findall('topic'):
            if a.attrib.get('name') == note[0]: # if the note topic already exists --> append 
                print("Appending to already existing topic...\t\t\t{}".format(get_time))
                new_note = ET.SubElement(a,'note', name=note[1])
                ET.SubElement(new_note, 'text').text = note[2]
                ET.SubElement(new_note, 'timestamp').text = note[3]
                tree.write('db.xml', encoding='UTF-8', xml_declaration=True)
                print("Topic appended \t\t\t{}".format(get_time()))
                return

        print("Creating new topic..\t\t\t {}".format(get_time()))
        new_topic = ET.SubElement(root,'topic', name=note[0])
        new_note = ET.SubElement(new_topic,'note', name=note[1])
        ET.SubElement(new_note, 'text').text = note[2]
        ET.SubElement(new_note, 'timestamp').text = note[3]
        tree.write('db.xml', encoding='UTF-8', xml_declaration=True)
        print("Created new topic. \t\t\t {}".format(get_time()))
        return True
    except:
        print("Error creating the note.\t\t\t {}".format(get_time()))
        return False



#registering the functions

server.register_function(get_topics)
server.register_function(find_topic)
server.register_function(create_topic)


# this basically enables multiple simultanous user requests
# not my code, but couldn't find the source afterwards

if __name__ == '__main__':
    try:
        print('Server started\t\t\t{}'.format(get_time()))
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
    except KeyboardInterrupt:
        print('Quitting server\t\t\t {}'.format(get_time()))