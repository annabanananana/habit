from datetime import date, datetime
from enum import Enum

class PeriodType(Enum):
    DAILY = 1
    WEEKLY = 2

class Habit:
    def __init__(self, name: str, periodType: PeriodType, creationDate: date):
        """Habit class to represent a habit."""
        self.name = name
        self.periodType = periodType
        self.creationDate = creationDate
        self.events = []  # Store all check-off events as a list of dates

    def execution(self, event_date: str = None):
        """Add an event to the habit."""
        if not event_date:
            event_date = str(date.today())
        self.events.append(event_date)

    def store(self, db):
        """Store the habit in the database."""
        cur = db.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO habit (name, periodType, creationDate) VALUES (?, ?, ?)",
            (self.name, self.periodType.value, self.creationDate),
        )
        db.commit()

    def add_event(self, db, event_date: str = None):
        """Store a new check-off event in the database and the habit's events list."""
        if not event_date:
            event_date = str(date.today())
        self.events.append(event_date)  # Add to the in-memory list
        cur = db.cursor()
        cur.execute("INSERT INTO tracker (date, habitName) VALUES (?, ?)", (event_date, self.name))
        db.commit()

    def load_events_from_db(self, db):
        """Load all events for this habit from the database."""
        cur = db.cursor()
        cur.execute("SELECT date FROM tracker WHERE habitName = ?", (self.name,))
        self.events = [row[0] for row in cur.fetchall()]

    def calculate_streak(self):
        """Calculate the current streak dynamically based on events."""
        if not self.events:
            return 0

        sorted_events = sorted(self.events)
        streak = 1
        streak_period = 7 if self.periodType == PeriodType.WEEKLY else 1
        prev_date = datetime.strptime(sorted_events[0], "%Y-%m-%d")

        for event in sorted_events[1:]:
            current_date = datetime.strptime(event, "%Y-%m-%d")
            if (current_date - prev_date).days <= streak_period:
                streak += 1
            else:
                streak = 1  # Reset streak if gap exceeds the period
            prev_date = current_date

        return streak


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
   