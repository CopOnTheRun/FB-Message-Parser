from bs4 import BeautifulSoup as b

class thread(object):
    """Contains a list of messages, as well as participants"""

    def __init__(self,threadDiv):
        self.people = set(threadDiv.next_element.split(', '))
        self.messages=[]
        for x in threadDiv.find_all(class_='message'):
            self.messages.append(message(x,x.next_sibling))

class message(object):
    """Contains the message text, sender, and date/time"""

    def __init__(self,messDiv,pDiv):
        self.text = pDiv.string
        self.sender = messDiv.find(class_='user').string
        self.timeDate = messDiv.find(class_='meta').string

def main():
    threads = []
    soup = b(open('messages.htm'))
    for x in soup.find_all(class_='thread'):
        threads.append(thread(x))
    for x in threads:
        print(x.people)

main()
