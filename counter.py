#import datetime
#import questionairy
from db import add_counter, increment_counter


class Counter:
    def __init__(self, name: str, description: str):
        """Counter class to count events
        :param name: name of the counter
        :param description: description of the counter
        """
        self.name = name
        self.description = description
        self.count = 0
    
    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def __str__(self):
        return f"{self.name}: {self.count}"

#maybe implement second class DB-counter?    
    def store(self, db):
        add_counter(db, self.name, self.description)

    def add_event(self, db, date: str = None):
        increment_counter(db, self.name, date)

'''counter = Counter("test_name", "test_description")
counter.increment()
print(counter)
'''


'''class Habit:
    def __init__(self, task, category, interval, date_created = None, date_due = None, date_completed = None, status = None, position = None):
        self.task = task
        self.category = category
        self.interval = interval
        self.date_created = date_created if date_created is not None else datetime.datetime.now()
        self.date_due = date_due if date_due is not None 
        self.date_completed = date_completed if date_completed is not None else datetime.datetime.now()
        self.status = status
        self.position = position
    
    def chose_interval(interval):
        if interval == "daily":

    
    def status():
'''
