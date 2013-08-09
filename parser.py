from bs4 import BeautifulSoup as b

class Thread(object):
    """Contains a list of messages, as well as participants"""

    def __init__(self,threadDiv):
        self.people = set(threadDiv.next_element.split(', '))
        self.messages=[]
        for x in threadDiv.find_all(class_='message'):
            self.messages.append(Message(x,x.next_sibling))

    def __str__(self):
        return '\nA conversation between {}\n{}\n{}'.format(self.people,self.messages,'~'*79)
    def __repr__(self):
        return '\nA conversation between {}\n{}\n{}'.format(self.people,self.messages,'~'*79)

class Message(object):
    """Contains the message text, sender, and date/time"""

    def __init__(self,messDiv,pDiv):
        self.text = pDiv.string
        self.sender = messDiv.find(class_='user').string
        self.timeDate = messDiv.find(class_='meta').string

    def __str__(self):
        return 'On {} {} said: {}'.format(self.timeDate,self.sender,self.text)
    def __repr__(self):
        return '\n{}\n{}\n{}'.format(self.timeDate,self.sender,self.text)

def main():
    threads = []
    soup = b(open('messages.htm'))
    for x in soup.find_all(class_='thread'):
        threads.append(Thread(x))
    print(threads)

main()
