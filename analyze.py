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


'''
from datetime import datetime, timedelta

def calculate_streaks(habit_obj):
    """
    Calculate the current and maximum streak for a habit based on its events.
    """
    event_dates = []
    for event in habit_obj.events:
        try:
            event_dates.append(datetime.strptime(event[0], '%Y-%m-%d'))
        except ValueError:
            print(f"Invalid date format: {event[0]}")
            continue  # Skip invalid date entries
    
    event_dates = sorted(event_dates)
    if not event_dates:
        return 0, 0  # No events, no streaks
    
    # Sort events by date
    #event_dates = sorted([datetime.strptime(event[0], '%Y-%m-%d') for event in habit_obj.events])
    
    # Define streak period based on habit type
    streak_period = timedelta(weeks=1) if habit_obj.period_type == PeriodType.WEEKLY else timedelta(days=1)
    
    max_streak = 1  # At least one event means a streak of 1
    current_streak = 1
    prev_date = event_dates[0]

    for current_date in event_dates[1:]:
        # Calculate the gap between events
        gap = (current_date - prev_date).days
        print(f"Comparing {prev_date.date()} with {current_date.date()} | Gap: {gap} days")
        
        if habit_obj.period_type == PeriodType.WEEKLY:
            # For weekly habits, reset the streak if the gap is more than 7 days
            if 0 < gap <= 7:
                current_streak += 1
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1  # Reset streak for weekly habits if the gap is more than 7 days
        else:
            # For daily habits, reset streak if the gap is more than 1 day
            if gap <= 1:
                current_streak += 1
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1  # Reset streak for daily habits if the gap is more than 1 day
        
        prev_date = current_date

    # Ensure the last streak is counted
    max_streak = max(max_streak, current_streak)

    # **Calculate ongoing streak**
    today = datetime.today()
    if (today - event_dates[-1]).days > 7 and habit_obj.period_type == PeriodType.WEEKLY:
        current_streak = 0  # Reset if last event is too old for weekly habits
    
    print(f"Final Max streak: {max_streak}, Final Current streak: {current_streak}")
    return current_streak, max_streak

'''


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


'''


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
            print(f"Checking habit: {habit.name}, {habit.period_type}")
            print(f"Checking habit: {habit.name}, Stored: {habit.period_type.name}, Expected: {period_type.name}")
            print(f"Type of habit.period_type: {type(habit.period_type)}, Type of period_type: {type(period_type)}")


            if PeriodTypeEnum[habit.period_type.name] == period_type:
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
'''
