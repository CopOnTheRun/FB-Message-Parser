from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import pickle, json
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
                    str(y.find(class_='user').string),
                    dt.strptime(y.find(class_='meta').string,dtFormat),
                    str(y.next_sibling.string)
                )
            )
        chatList.append(
            fb_chat.Thread(
                set(x.next_element.split(', ')),
                threadList
            )
        )
    return fb_chat.Chat(chatList)

def jsonEncode(pyObj):
    '''This is the method to be passed into the 'default' argument of json.dump.'''

    if isinstance(pyObj, fb_chat.Chat):
        return {'threads':pyObj.threads}
    elif isinstance(pyObj, fb_chat.Thread):
        return {'messages':pyObj.messages,
                'people':pyObj.people}
    elif isinstance(pyObj, fb_chat.Message):
        return {'text':pyObj.text,
                'date_time':pyObj.date_time,
                'sender':pyObj.sender}
    elif isinstance(pyObj, dt):
        return pyObj.strftime(dtFormat)
    elif isinstance(pyObj, set):
        return list(pyObj)
    raise TypeError('{} is not JSON serializable'.format(repr(pyObj)))

def pyToJson(pyObj,name='messages.json'):
	with open(name,'w') as f:
		json.dump(pyObj,f,default=jsonEncode,indent=2)

def pyToPickle(pyObj,name='messages.pickle'):
	'''This method will picklize our python object for easy access later'''
	with open(name,'wb') as f:
		pickle.dump(pyObj,f)

def pickleToPy(name='messages.pickle'):
	with open(name,'rb') as f:
		return pickle.load(f)
