import json
import pickle
from datetime import datetime as dt

from bs4 import BeautifulSoup as bs

import fb_chat


#dtFormat = '%A, %B %d, %Y at %I:%M%p %Z'
dtFormat = '%A, %d %B %Y at %H:%M %Z'  # UK Format

def html_to_py(file):
    soup = bs(file)
    chat_list = []
    for x in soup.find_all(class_='thread'):
        thread_list = []
        for y in x.find_all(class_='message'):
            thread_list.append(
                fb_chat.Message(
                    y.find(class_='user').string,
                    # Remove "+01" in some dates, to just use BST timezone:
                    dt.strptime(y.find(class_='meta').string.replace("+01", ""), dtFormat),
                    y.next_sibling.string
                )
            )
        chat_list.append(
            fb_chat.Thread(
                set(x.next_element.split(', ')),
                thread_list
            )
        )
    return fb_chat.Chat(chat_list)


def json_encode(py_obj):
    """This is the method to be passed into the 'default' argument
    of json.dump."""

    if isinstance(py_obj, fb_chat.Chat):
        return {'threads': py_obj.threads}
    elif isinstance(py_obj, fb_chat.Thread):
        return {'messages': py_obj.messages,
                'people': py_obj.people}
    elif isinstance(py_obj, fb_chat.Message):
        return {'text': py_obj.text,
                'date_time': py_obj.date_time,
                'sender': py_obj.sender}
    elif isinstance(py_obj, dt):
        return py_obj.strftime(dtFormat)
    elif isinstance(py_obj, set):
        return list(py_obj)
    raise TypeError('{} is not JSON serializable'.format(repr(py_obj)))


def py_to_json(py_obj, name='messages.json'):
    with open(name, 'w') as f:
        json.dump(py_obj, f, default=json_encode, indent=2)


def py_to_pickle(py_obj, name='messages.pickle'):
    """ This method will picklize our python object for easy access later """
    with open(name, 'wb') as f:
        pickle.dump(py_obj, f)


def pickle_to_py(name='messages.pickle'):
    with open(name, 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    # So long as "messages.htm" in same directory: runs automatically
    with open('messages.htm', "r") as f:
        Chat = html_to_py(f)
        # Dump to json to prove works:
        py_to_json(Chat)
