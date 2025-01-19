from db import get_habit_data
from datetime import datetime, timedelta

def calculate_count(db, habit_name):
    """Calculates the total number of events for a habit"""
    data = get_habit_data(db, habit_name)
    return len(data)

def calculate_streak(db, habit_name, period_type):
    """
    Calculates the longest streak of events for a habit.

    :param db: SQLite database connection
    :param habit_name: Name of the habit
    :param period_type: PeriodType (DAILY or WEEKLY)
    :return: Longest streak count
    """
    data = get_habit_data(db, habit_name)
    if not data:
        return 0

    # Convert event dates to datetime objects and sort them
    dates = sorted([datetime.strptime(row[0], "%Y-%m-%d") for row in data])

    streak = 1
    max_streak = 1
    for i in range(1, len(dates)):
        current_date = dates[i]
        prev_date = dates[i - 1]

        if period_type == "DAILY":
            # Check if the current date is exactly 1 day after the previous date
            if (current_date - prev_date).days == 1:
                streak += 1
            else:
                max_streak = max(max_streak, streak)
                streak = 1

        elif period_type == "WEEKLY":
            # Check if the current date is exactly 7 days after the previous date
            if (current_date - prev_date).days == 7:
                streak += 1
            else:
                max_streak = max(max_streak, streak)
                streak = 1

    return max(max_streak, streak)



'''
from db import get_habit_data

def calculate_count(db, habit):
    """
    Calculate the count of the counter.
    
    :param db: an initialized sqlite3 database connection
    :param counter: name of the counter present in the DB
    :return: length of the counter increment events
    """
    data = get_habit_data(db, habit)
    #calculate consecutive checkoffs/counting events of habit
    return len(data)
'''