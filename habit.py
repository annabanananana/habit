from datetime import datetime
#import questionairy
from db import add_counter, increment_counter
from enum import Enum

#testcomment
class PeriodType(Enum):
    DAILY = 1
    WEEKLY = 2

class Habit:
    def __init__(self, name: str, periodType: PeriodType, creationDate: datetime):
        """Counter class to count events
        :param name: name of the counter
        :param description: description of the counter
        """
        self.name = name
        self.periodType = periodType
        self.creationDate = creationDate
    
   