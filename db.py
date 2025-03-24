import sqlite3
from sqlite3 import OperationalError
from datetime import date
from habit import PeriodType


# establishing db connection
def get_db(name="main.db"):
    try:
        db = sqlite3.connect(name)
        # db.execute("PRAGMA foreign_keys = ON;")  # Enabling foreign key constraints
        create_tables(db)
        return db
    except OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None


def create_tables(db):
    # creating tables for habit and tracker
    cur = db.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS habit (
                name TEXT PRIMARY KEY,
                periodType TEXT,
                creationDate TEXT)"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS tracker (
                date TEXT,
                habitName TEXT,
                FOREIGN KEY (habitName) REFERENCES habit(name))"""
    )
    db.commit()


def add_counter(db, name, period_type):
    """Adds a new habit to the habit table"""
    cur = db.cursor()
    cur.execute("INSERT INTO habit VALUES (?, ?, ?)", (name, period_type.name, date.today().isoformat()))
    db.commit()


def habit_exists(db, name):
    """Check if a habit exists in the database."""
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM habit WHERE name = ?", (name,))
    return cur.fetchone()[0] > 0


def add_event_habit(db, name, event_date=None):
    """Logs a habit event in the tracker table."""
    if not habit_exists(db, name):
        raise ValueError(f"Habit '{name}' does not exist in the database.")

    if not event_date:
        event_date = str(date.today())

    cur = db.cursor()
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (date.fromisoformat(event_date).isoformat(), name))
    db.commit()


def get_habit_data(db, name):
    """Fetches all habit events for a specific habit"""
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE habitName=?", (name,))
    return cur.fetchall()
