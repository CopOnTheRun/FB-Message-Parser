from bs4 import BeautifulSoup as b
import datetime as dt


class FbMsg(object):
    """Contains a list of Threads"""

    def __init__(self, fileName):
        self.threads = []
        soup = b(open(fileName))
        for x in soup.find_all(class_='thread'):
            self.threads.append(Thread(x))
    
    def __getitem__(self, key):
        return self.threads[key]


class Thread(object):
    """Contains a list of messages, as well as participants"""

    def __init__(self,threadDiv):
        self.people = set(threadDiv.next_element.split(', '))
        self.messages=[]
        for x in threadDiv.find_all(class_='message'):
            self.messages.append(Message(x,x.next_sibling))
    
    def __getitem__(self, key):
        return self.messages[key]

    def __str__(self):
        return '\nA conversation between {}\n{}\n{}'.format(self.people,self.messages,'~'*79)

    def __repr__(self):
        return '\nA conversation between {}\n{}\n{}'.format(self.people,self.messages,'~'*79)


class Message(object):
    """Contains the message text, sender, and date/time"""

    def __init__(self,messDiv,pDiv):
        self.text = pDiv.string
        self.sender = messDiv.find(class_='user').string
        dtFormat = '%A, %B %d, %Y at %I:%M%p %Z'
        self.date_time = dt.datetime.strptime(messDiv.find(class_='meta').string,dtFormat)

    def __str__(self):
        return 'On {} {} said: {}'.format(self.date_time,self.sender,self.text)

    def __repr__(self):
        return '\n{}\n{}\n{}'.format(self.date_time,self.sender,self.text)
