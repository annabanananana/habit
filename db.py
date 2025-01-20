import sqlite3
from sqlite3 import OperationalError
from datetime import date

def get_db(name="test.db"):
    try:
        db = sqlite3.connect(name)
        create_tables(db)
        return db
    except OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables(db):
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
                name TEXT PRIMARY KEY,
                periodType INTEGER,
                creationDate TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
                date TEXT,
                habitName TEXT,
                FOREIGN KEY (habitName) REFERENCES habit(name))""")
    db.commit()

def add_counter(db, name, period_type):
    """Adds a new habit to the habit table"""
    cur = db.cursor()
    cur.execute("INSERT INTO habit VALUES (?, ?, ?)", (name, period_type, str(date.today())))
    db.commit()

def execution_habit(db, name, event_date=None):
    """Logs a habit event in the tracker table"""
    cur = db.cursor()
    if not event_date:
        event_date = str(date.today())
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name))
    db.commit()

def get_habit_data(db, name):
    """Fetches all habit events for a specific habit"""
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE habitName=?", (name,))
    return cur.fetchall()


'''
import sqlite3
from datetime import date


def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
                name TEXT PRIMARY KEY,
                periodType INTEGER,
                creationDate TEXT)""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
                date TEXT,
                habitName TEXT,
                FOREIGN KEY (habitName) REFERENCES habit(name))""")
    db.commit()

def add_counter(db, name, description):
    cur = db.cursor()
    cur.execute("INSERT INTO counter VALUES (?, ?)", (name, description))
    db.commit()


def execution_habit(db, name, event_date=None):
    cur = db.cursor()
    if not event_date:
        event_date = str(date.today())
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name))
    db.commit()

#use try and except if name does not exist for example
def get_habit_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE counterName=?", (name,))
    return cur.fetchall()

'''
'''db = get_db()
create_tables(db)
'''