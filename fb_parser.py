from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import fb_chat

dtFormat = '%A, %B %d, %Y at %I:%M%p %Z'
def htmlToPy(file):
    soup = bs(file)
    chatList = []
    for x in soup.find_all(class_='thread'):
        threadList = []
        for y in x.find_all(class_='message'):
            threadList.append(
                fb_chat.Message(
                    y.find(class_='user').string,
                    dt.strptime(y.find(class_='meta').string,dtFormat),
                    y.next_sibling.string
                )
            )
        chatList.append(
            fb_chat.Thread(
                set(x.next_element.split(', ')),
                threadList
            )
        )
    return fb_chat.Chat(chatList)

def pyToJson(pyObj):
    '''This is the method to be passed into the 'default' argument of json.dump.'''

    if isinstance(pyObj, fb_chat.Chat):
        return {'threads':pyObj.threads}
    elif isinstance(pyObj, fb_chat.Thread):
        return {'people':pyObj.people,
                'messages':pyObj.messages}
    elif isinstance(pyObj, fb_chat.Message):
        return {'sender':pyObj.sender,
                'date_time':pyObj.date_time,
                'text':pyObj.text}
    elif isinstance(pyObj, dt):
        return pyObj.strftime(dtFormat)
    elif isinstance(pyObj, set):
        return list(pyObj)
    raise TypeError('{} is not JSON serializable'.format(repr(pyObj)))
