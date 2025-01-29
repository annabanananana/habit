from datetime import date
from enum import Enum

class PeriodType(Enum):
    """PeriodType class for daily and weekly habits."""
    DAILY = 1
    WEEKLY = 2

class Habit:
    def __init__(self, name: str, periodType: PeriodType, creationDate: date):
        """Habit class to represent a habit.
        :param name: name of habit
        :param periodType: daily or weekly period Type
        :param creationDate: date of habit creation
        :param events: list of dates habit was executed"""
        self.name = name
        self.periodType = periodType
        self.creationDate = creationDate
        self.events = []  # Store all check-off events as a list of dates

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

   
    @classmethod
    def load_all_habits(cls, db):
        """Load all habits from the database."""
        try:
            cursor = db.cursor()
            cursor.execute("SELECT name, periodType, creationDate FROM habit")
            habits = cursor.fetchall()  # Fetch all habits from the database

            habit_objects = []
            for name, period, creation_date in habits:
                try:
                # Create a Habit instance for each habit in the database
                    habit = cls(name, PeriodType(period), creationDate=creation_date)
                    habit.load_events_from_db(db)  # Load the events for the habit
                    habit_objects.append(habit)
                except Exception as e:
                    print(f"Error loading habit '{name}': {e}")
                    continue  # Skip problematic habits

            return habit_objects

        except Exception as e:
            print(f"Error loading habits from database: {e}")
            return []
    
    def load_events_from_db(self, db):
        """Load all events for this habit from the database."""
        cur = db.cursor()
        cur.execute("SELECT date FROM tracker WHERE habitName = ?", (self.name,))
        self.events = [row[0] for row in cur.fetchall()]
     

'''

from datetime import date, datetime
from enum import Enum

class PeriodType(Enum):
    """PeriodType class for daily and weekly habits."""
    DAILY = 1
    WEEKLY = 2

class Habit:
    def __init__(self, name: str, periodType: PeriodType, creationDate: date):
        """Habit class to represent a habit.
        :param name: name of habit
        :param periodType: daily or weekly period Type
        :param cretaion Date: date of habit creation
        :param events: list of dates habit was executed"""
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

    @classmethod
    def load_all_habits(cls, db):
        """Load all habits from the database."""
        cursor = db.cursor()
        cursor.execute("SELECT name, description, period, creation_date FROM habits")
        habit = cursor.fetchall()  # Fetch all habits from the database

        habit_objects = []
        for name, description, period, creation_date in habit:
        # Create a Habit instance for each habit in the database
            habit = cls(name, PeriodType(period), creationDate=creation_date)
            habit.load_events_from_db(db)  # Load the events for the habit
            habit_objects.append(habit)

        return habit_objects
'''