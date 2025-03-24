from db import get_habit_data
import traceback
from habit import Habit, PeriodType
from datetime import datetime, timedelta
from enum import Enum


class PeriodTypeEnum(Enum):
    DAILY = 1
    WEEKLY = 2


def get_habits_by_periodicity(db_connection, period_type):
    """
    Retrieve a list of habits filtered by their periodicity.

    :param db: Database connection object
    :param period_type: PeriodType (DAILY or WEEKLY)
    :return: List of habit names matching the periodicity
    """
    try:
        habits = Habit.load_all_habits(db_connection)
        print(f"Loaded habits: {habits} , Period type: {period_type}")
        filtered_habits = [habit for habit in habits if habit.period_type == period_type]
        return filtered_habits
    except Exception as e:
        print(f"Error retrieving habits by periodicity: {e}")
        return []


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


def calculate_streaks(habit_obj) -> tuple[int, int]:
    """
    Calculate the current and maximum streak for a habit based on its events.

    :param habit_obj: The Habit object with loaded events
    :return: A tuple (current_streak, max_streak)
    """
    if not habit_obj.events:
        return 0, 0  # No events, no streaks

    try:
        # Convert event strings to datetime objects and sort them
        event_dates = sorted(
            (datetime.fromisoformat(event) if isinstance(event, str) else event) for event in habit_obj.events if event
        )

        # Define streak period based on habit type
        # streak_period = timedelta(days=8) if habit_obj.period_type == PeriodTypeEnum.WEEKLY else timedelta(days=1)

        max_streak = 1  # At least one event means a streak of 1
        current_streak = 1
        prev_date = event_dates[0]

        for current_date in event_dates[1:]:  # missing day 1
            # Debugging output
            print(f"Comparing {prev_date} with {current_date}")
            gap = (current_date - prev_date).days
            print(f"Gap: {gap} days")
            print(f"Period type: {habit_obj.period_type}")
            # Explicitly allow exactly 7-day gaps for weekly habits, must be == 7 or == 1
            if gap <= (
                7 if habit_obj.period_type == PeriodType.WEEKLY else 1
            ):  # 7 days for weekly, 1 day for daily or adjust for different gaps
                current_streak += 1
                print(f"Streak increased to {current_streak}")
            else:
                max_streak = max(max_streak, current_streak)
                print(f"Streak reset. Max streak: {max_streak}")
                current_streak = 1  # Reset streak
            prev_date = current_date

        max_streak = max(max_streak, current_streak)  # Ensure last streak is counted

        # **Calculate ongoing streak**  new function!
        today = datetime.today()
        if (today - event_dates[-1]).days > gap:
            current_streak = 0  # Reset if last event is too old

        return current_streak, max_streak

    except Exception as e:
        print(f"Error calculating streaks: {e}")
        return 0, 0


def get_longest_streak(db_connection, period_type) -> list[tuple[str, int]]:
    """
    Determine all habits with the longest run streak for a given period type (daily or weekly).

    :param db_connection: Database connection object
    :param period_type: PeriodTypeEnum (DAILY or WEEKLY)
    :return: List of tuples [(habit_name, longest_streak), ...]
    """
    try:
        habits = Habit.load_all_habits(db_connection)
        longest_streak = 0
        longest_habits = []  # Store all habits with the same longest streak

        for habit in habits:
            if PeriodTypeEnum[habit.period_type.name] == period_type:
                habit.load_events(db_connection)
                max_streak = calculate_streaks(habit)

                if isinstance(max_streak, tuple):  # Ensure compatibility
                    _, max_streak = max_streak

                if max_streak > longest_streak:
                    longest_streak = max_streak
                    longest_habits = [(habit.name, max_streak)]  # Reset and add new leader
                elif max_streak == longest_streak and max_streak > 0:
                    longest_habits.append((habit.name, max_streak))  # Add to existing leaders

        return longest_habits  # Return a list of all top habits

    except Exception as e:
        print(f"Error determining longest {period_type.name.lower()} run streak: {e}")
        traceback.print_exc()
        return []


# Usage:
def get_longest_daily_run_streak(db_connection):
    return get_longest_streak(db_connection, PeriodTypeEnum.DAILY)


def get_longest_weekly_run_streak(db_connection):
    return get_longest_streak(db_connection, PeriodTypeEnum.WEEKLY)


def get_longest_overall_run_streak(db_connection) -> list[tuple[str, int]]:
    """
    Determine all habits with the longest run streak overall (daily and weekly combined)
    return get_longest_streak(db_connection, PeriodTypeEnum.DAILY) + get_longest_streak(
    :param db_connection: Database connection object
    :param period_type: PeriodTypeEnum (DAILY or WEEKLY)
    :return: List of tuples [(habit_name, longest_streak), ...]
    """
    try:
        habits = Habit.load_all_habits(db_connection)
        longest_streak = 0
        longest_habits = []  # Store all habits with the same longest streak

        for habitPeriodtype in PeriodTypeEnum:
            for habit in habits:
                if PeriodTypeEnum[habit.period_type.name] == habitPeriodtype:
                    habit.load_events(db_connection)
                    max_streak = calculate_streaks(habit)

                    if isinstance(max_streak, tuple):  # Ensure compatibility
                        _, max_streak = max_streak

                    if max_streak > longest_streak:
                        longest_streak = max_streak
                        longest_habits = [(habit.name, max_streak)]  # Reset and add new leader
                    elif max_streak == longest_streak and max_streak > 0:
                        longest_habits.append((habit.name, max_streak))  # Add to existing leaders

        return longest_habits  # Return a list of all top habits

    except Exception as e:
        print(f"No longest streak run available: {e}")
        traceback.print_exc()
        return []
