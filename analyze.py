from db import get_habit_data
from habit import Habit
from datetime import datetime
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

    :param habit: The Habit object with loaded events
    :return: A tuple (current_streak, max_streak)
    """
    if not habit_obj.events:
        return 0, 0  # No events, so no streaks

    try:
        # Sort events in ascending order
        sorted_events = sorted(habit_obj.events)
        current_streak = 1
        max_streak = 1
        streak_period = 7 if habit_obj.period_type == PeriodTypeEnum.WEEKLY else 1
        prev_date = datetime.strptime(sorted_events[0], "%Y-%m-%d")

        for event in sorted_events[1:]:
            current_date = datetime.strptime(event, "%Y-%m-%d")
            # Check if the gap between events is within the allowed streak period
            if (current_date - prev_date).days <= streak_period:
                current_streak += 1
                max_streak = max(max_streak, current_streak)  # Update max streak
            else:
                current_streak = 1  # Reset current streak if gap exceeds the period
            prev_date = current_date

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


def get_longest_run_streak(db_connection):
    """
    Determine the longest run streak among all habits.

    :param db: Database connection object
    :return: Tuple (habit, max_streak)
    """
    try:
        habits = Habit.load_all_habits(db_connection)
        longest_streak = 0
        longest_habit = None

        for habit in habits:
            habit.load_events(db_connection)
            _, max_streak = calculate_streaks(habit)
            if max_streak > longest_streak:
                longest_streak = max_streak
                longest_habit = habit

        return longest_habit, longest_streak
    except Exception as e:
        print(f"Error determining longest run streak: {e}")
        return None, 0

