from datetime import date
from enum import Enum

class PeriodType(Enum):
    DAILY = 1
    WEEKLY = 2

class Habit:
    def __init__(self, name: str, periodType: PeriodType, creationDate: date):
        """Counter class to count events
        :param name: name of the habit
        :param periodType: type of the habit period (e.g., DAILY, WEEKLY)
        :param creationDate: date of habit creation
        """
        self.name = name
        self.periodType = periodType
        self.creationDate = creationDate
        self.count = 0

    def execution(self):
        """Increments the habit count"""
        self.count += 1

    def __str__(self):
        return f"{self.name}: {self.count}"

    def add_event(self, db, date: str = None):
        """Adds a habit event to the tracker database"""
        from db import execution_habit
        execution_habit(db, self.name, date)



'''from datetime import date
import time
#import questionairy
from db import add_counter, execution_habit
from enum import Enum

#testcomment
class PeriodType(Enum):
    DAILY = 1
    WEEKLY = 2

class Habit:
    def __init__(self, name: str, periodType: PeriodType, creationDate: date):
        """Counter class to count events
        :param name: name of the counter
        :param description: description of the counter
        """
        self.name = name
        self.periodType = periodType
        self.creationDate = date.today()
        self.count = 0

    def execution(self):
        self.count += 1
    
    def __str__(self):
        return f"{self.name}: {self.count}"

    def add_event(self, db, date: str = None):
        execution_habit(db, self.name, date)
'''
   