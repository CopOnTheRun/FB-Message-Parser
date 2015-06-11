class Chat(object):
    """Contains a list of Threads"""

    def __init__(self, threads):
        self.threads = threads
        self.personDict = {person: self.__by(person) for person in
                           {ppl for thread in self for ppl in thread.people}}
        self.messages = sorted([y for x in self.threads for y in x])

    def __getitem__(self, key):
        if type(key) is int: return self.threads[key]
        elif type(key) is str: return self.personDict[key]

    def __repr__(self): return '<FbMsg len(threads)={}>'.format(len(self))

    def __len__(self): return len(self.threads)

    # returns a date-sorted list of messages sent by "name"
    def __by(self, name):
        return sorted([msg for thread in self
                       if name in thread.people
                       for msg in thread.by(name)])

    def sent_before(self, date):
        return [msg for thread in self for msg in thread.sent_before(date)]

    def sent_after(self, date):
        return [msg for thread in self for msg in thread.sent_after(date)]

    def sent_between(self,beg,end):
        return [msg for thread in self for msg in thread.sent_between(beg,end)]


class Thread(object):
    """Contains a list of people included, and messages """

    def __init__(self,people,messages):
        self.people = people
        self.messages = messages

    def __getitem__(self, key): return self.messages[key]

    def __repr__(self):
        return '<Thread people={}, len(messages)={}>'.\
            format(self.people, len(self.messages))

    def __str__(self): return '{}\n{}\n'.format(self.people, self.messages)

    def __len__(self): return len(self.messages)

    def by(self, name):
        return [msg for msg in self if msg.sent_by(name)]

    def sent_before(self, date):
        return [msg for msg in self if msg.sent_before(date)]

    def sent_after(self, date):
        return [msg for msg in self if msg.sent_after(date)]

    def sent_between(self, beg, end):
        return [msg for msg in self if msg.sent_between(beg, end)]


class Message(object):
    """Contains the message text, sender, and date/time"""

    def __init__(self, sender, date_time, text):
        self.sender = sender
        self.date_time = date_time
        self.text = text

    def __repr__(self):
        return '<Message date_time={} sender={} text={}'.format(
            self.date_time, self.sender, self.text)

    def __str__(self):
        return '{}\n{}\n{}\n'.format(self.sender, self.date_time, self.text)

    def __lt__(self, message):
        return self.sent_before(message.date_time)

    def __gt__(self, message):
        return self.sent_after(message.date_time)

    def __eq__(self, message):
        return self.date_time == message.date_time

    def sent_by(self, name):
        return self.sender == name

    def sent_before(self,date):
        try:
            return self.date_time < date
        except TypeError:
            return self.date_time.date() < date

    def sent_after(self,date):
        try:
            return self.date_time > date
        except TypeError:
            return self.date_time.date() > date

    def sent_between(self, beg, end):
        return self.sent_after(beg) and self.sent_before(end)
