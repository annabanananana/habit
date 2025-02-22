from db import get_habit_data
import traceback
from habit import Habit
from datetime import datetime, timedelta
from enum import Enum


class PeriodTypeEnum(Enum):
    DAILY = 1
    WEEKLY = 2


def calculate_count(db_connection, habit_name):
    """
    Calculate the total number of events for a habit.

    :param db: Database connection object
    :param habit_name: Name of the habit
    :return: Total count of events
    """
    try:
        data = get_habit_data(db_connection, habit_name)
        return len(data)
    except Exception as e:
        print(f"Error calculating event count: {e}")
        return 0


def calculate_streaks(habit_obj):
    """
    Calculate the current and maximum streak for a habit based on its events.

    :param habit_obj: The Habit object with loaded events
    :return: A tuple (current_streak, max_streak)
    """
    if not habit_obj.events:
        return 0, 0  # No events, no streaks

    try:
        # Convert event strings to datetime objects and sort them
        event_dates = sorted(datetime.fromisoformat(event) for event in habit_obj.events if isinstance(event, str) and event)

        # Define streak period based on habit type
        streak_period = timedelta(days=7) if habit_obj.period_type == PeriodTypeEnum.WEEKLY else timedelta(days=1)

        max_streak = 1  # At least one event means a streak of 1
        current_streak = 1
        prev_date = event_dates[0]

        for current_date in event_dates[1:]:
            if (current_date - prev_date).days <= streak_period.days:
                current_streak += 1
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1  # Reset streak
            prev_date = current_date

        max_streak = max(max_streak, current_streak)  # Ensure last streak is counted

        # **Calculate ongoing streak**
        today = datetime.today()
        if (today - event_dates[-1]).days > streak_period.days:
            current_streak = 0  # Reset if last event is too old

        return current_streak, max_streak

    except Exception as e:
        print(f"Error calculating streaks: {e}")
        return 0, 0

def get_habits_by_periodicity(db_connection, period_type):
    """
    Retrieve a list of habits filtered by their periodicity.

    :param db: Database connection object
    :param period_type: PeriodType (DAILY or WEEKLY)
    :return: List of habit names matching the periodicity
    """
    try:
        habits = Habit.load_all_habits(db_connection)
        filtered_habits = [habit for habit in habits if habit.period_type == period_type]
        return filtered_habits
    except Exception as e:
        print(f"Error retrieving habits by periodicity: {e}")
        return []



def get_longest_streak(db_connection, period_type):
    """
    Determine the longest run streak for a given period type (daily or weekly).

    :param db_connection: Database connection object
    :param period_type: PeriodTypeEnum (DAILY or WEEKLY)
    :return: Tuple (longest_habit_name, longest_streak)
    """
    try:
        habits = Habit.load_all_habits(db_connection)
        longest_streak = 0
        longest_habit_name = None

        for habit in habits:
            if habit.period_type == period_type:
                habit.load_events(db_connection)
                max_streak = calculate_streaks(habit)
                if isinstance(max_streak, tuple):  # Ensure compatibility
                    _, max_streak = max_streak  

                if max_streak > longest_streak:
                    longest_streak = max_streak
                    longest_habit_name = habit.name

        return longest_habit_name, longest_streak

    except Exception as e:
        print(f"Error determining longest {period_type.name.lower()} run streak: {e}")
        traceback.print_exc()
        return None, 0

# Usage:
def get_longest_daily_run_streak(db_connection):
    return get_longest_streak(db_connection, PeriodTypeEnum.DAILY)

def get_longest_weekly_run_streak(db_connection):
    return get_longest_streak(db_connection, PeriodTypeEnum.WEEKLY)