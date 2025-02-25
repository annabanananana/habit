from datetime import date
from enum import Enum

class PeriodType(Enum):
    """PeriodType class for daily and weekly habits."""
    DAILY = "daily"
    WEEKLY = "weekly"

class Habit:
    def __init__(self, name: str, period_type: PeriodType, creation_date: date):
        """Habit class to represent a habit.
        :param name: name of habit
        :param period_type: daily or weekly period type
        :param creation_date: date of habit creation
        :param events: list of dates habit was executed"""
        self.name = name
        self.period_type = period_type
        self.creation_date = creation_date
        self.events = []  # Store all check-off events as a list of dates

    def store(self, db):
        """Store the habit in the database."""
        cur = db.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO habit (name, periodType, creationDate) VALUES (?, ?, ?)",
            (self.name, self.period_type.value, self.creation_date),
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
                    habit = cls(name, PeriodType(period), creation_date=creation_date)
                    habit.load_events(db)  # Load the events for the habit
                    habit_objects.append(habit)
                except Exception as e:
                    print(f"Error loading habit '{name}': {e}")
                    continue  # Skip problematic habits

            return habit_objects

        except Exception as e:
            print(f"Error loading habits from database: {e}")
            return []
 
    def load_events(self, db):
        """Load all events from the database."""
        cursor = db.cursor()
        cursor.execute("SELECT date FROM tracker WHERE habitName = ?", (self.name,))
        self.events = [row[0] for row in cursor.fetchall()]

