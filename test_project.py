import os
import importlib
from db import get_db, add_counter, add_event_habit, get_habit_data
from habit import Habit, PeriodType
import habit
importlib.reload(habit)
from analyze import calculate_count, calculate_streaks, get_longest_run_streak
from datetime import datetime

class TestHabitTracker:
    def setup_method(self):
        # Setup the test database
        self.db = get_db("test.db")

        # Add sample habits (3 daily habits, 2 weekly habits)
        add_counter(self.db, "daily_habit_1", 1)
        add_counter(self.db, "daily_habit_2", 1)
        add_counter(self.db, "daily_habit_3", 1)
        add_counter(self.db, "weekly_habit_1", 2)
        add_counter(self.db, "weekly_habit_2", 2)

        # Add events for each habit over the past 6 weeks
        dates_daily_1 = ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]
        for date in dates_daily_1:
            add_event_habit(self.db, "daily_habit_1", date)

        dates_daily_2 = ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-05"]
        for date in dates_daily_2:
            add_event_habit(self.db, "daily_habit_2", date)

        dates_daily_3 = ["2025-01-01", "2025-01-03", "2025-01-05"]
        for date in dates_daily_3:
            add_event_habit(self.db, "daily_habit_3", date)

        dates_weekly_1 = ["2024-12-15", "2024-12-22", "2024-12-29", "2025-01-05"]
        for date in dates_weekly_1:
            add_event_habit(self.db, "weekly_habit_1", date)

        dates_weekly_2 = ["2024-12-16", "2024-12-23", "2024-12-30", "2025-01-06"]
        for date in dates_weekly_2:
            add_event_habit(self.db, "weekly_habit_2", date)

    def test_calculate_count(self):
        # Test the calculate_count function for different habits
        count_1 = calculate_count(self.db, "daily_habit_1")
        count_2 = calculate_count(self.db, "daily_habit_2")
        count_3 = calculate_count(self.db, "daily_habit_3")
        count_4 = calculate_count(self.db, "weekly_habit_1")
        count_5 = calculate_count(self.db, "weekly_habit_2")

        assert count_1 == 5  # Should have 5 events for daily_habit_1
        assert count_2 == 4  # Should have 4 events for daily_habit_2
        assert count_3 == 3  # Should have 3 events for daily_habit_3
        assert count_4 == 4  # Should have 4 events for weekly_habit_1
        assert count_5 == 4  # Should have 4 events for weekly_habit_2

    def test_calculate_streaks(self):
        # Ensure today's date is within the event data range
        today = datetime.today().strftime('%Y-%m-%d')
    
        # Test the calculate_streaks function for daily habits
        habit_1 = Habit("daily_habit_1", PeriodType.DAILY, creationDate="2025-01-01")
        habit_1.load_events(self.db)
        habit_1.add_event(self.db, today)  # Add today's event explicitly for the test
        current_streak_1, max_streak_1 = calculate_streaks(habit_1)

        habit_2 = Habit("daily_habit_2", PeriodType.DAILY, creationDate="2025-01-01")
        habit_2.load_events(self.db)
        current_streak_2, max_streak_2 = calculate_streaks(habit_2)

        habit_3 = Habit("daily_habit_3", PeriodType.DAILY, creationDate="2025-01-01")
        habit_3.load_events(self.db)
        current_streak_3, max_streak_3 = calculate_streaks(habit_3)

        # Print debugging information
        print(f"habit_1: Current streak: {current_streak_1}, Max streak: {max_streak_1}")
        print(f"habit_2: Current streak: {current_streak_2}, Max streak: {max_streak_2}")
        print(f"habit_3: Current streak: {current_streak_3}, Max streak: {max_streak_3}")

        # Validate streaks for daily habits
        assert current_streak_1 == 1  # Last event is today, current streak = 1
        assert max_streak_1 == 5  # Max streak for daily_habit_1 is 5
        assert current_streak_2 == 0  # Last event is 2 days ago, current streak = 1
        assert max_streak_2 == 3  # Max streak for daily_habit_2 is 4
        assert current_streak_3 == 0  # Last event is 2 days ago, current streak = 1
        assert max_streak_3 == 1  # Max streak for daily_habit_3 is 3


        # Test the calculate_streaks function for weekly habits
        habit_weekly_1 = Habit("weekly_habit_1", PeriodType.WEEKLY, creationDate="2024-12-15")
        habit_weekly_1.load_events(self.db)
        current_streak_weekly_1, max_streak_weekly_1 = calculate_streaks(habit_weekly_1)

        habit_weekly_2 = Habit("weekly_habit_2", PeriodType.WEEKLY, creationDate="2024-12-16")
        habit_weekly_2.load_events(self.db)
        current_streak_weekly_2, max_streak_weekly_2 = calculate_streaks(habit_weekly_2)

        print(f"habit_weekly_1: Current streak: {current_streak_weekly_1}, Max streak: {max_streak_weekly_1}")
        print(f"habit_weekly_2: Current streak: {current_streak_weekly_2}, Max streak: {max_streak_weekly_2}")

        # Validate streaks for weekly habits
        assert current_streak_weekly_1 == 0  # Last event is within the streak period
        assert max_streak_weekly_1 == 1  # Max streak for weekly_habit_1 is 1
        assert current_streak_weekly_2 == 0  # Last event is within the streak period
        assert max_streak_weekly_2 == 1  # Max streak for weekly_habit_2 is 1

    def test_get_longest_run_streak(self):
        # Test the get_longest_run_streak function with predefined habits and events
        longest_streak_habit, longest_streak = get_longest_run_streak(self.db)

        # Debugging information
        print(f"Longest streak habit: {longest_streak_habit}, Longest streak: {longest_streak}")

        # Validate the longest streak data
        assert sorted(longest_streak_habit) == sorted(["daily_habit_1"])  # Habit with the longest streak
        assert longest_streak == 5  # Maximum streak for daily_habit_1

    def teardown_method(self):
        # Close the database connection and remove the test database
        if self.db:
            self.db.close()

        if os.path.exists("test.db"):
            os.remove("test.db")  # Clean up the test database after testing

'''
import os
#import pytest
import importlib
from db import get_db, add_counter, add_event_habit, get_habit_data
from habit import Habit, PeriodType
import habit
importlib.reload(habit)
from analyze import calculate_count, calculate_streaks, get_longest_run_streak

print(f"Habit class: {Habit}")
#testing the habit tracker app with pre-defined habits and dates.
#Careful: check assertions before running, since they change due to changing date of "today".
class TestHabitTracker:

    def setup_method(self):
        # Setup the test database
        self.db = get_db("test.db")

        # Add sample habits (5 habits: daily, weekly)
        add_counter(self.db, "daily_habit", 1)
        add_counter(self.db, "weekly_habit", 2)
        add_counter(self.db, "daily_habit_2", 1)
        add_counter(self.db, "weekly_habit_2", 2)

        # Add events for each habit over the past 6 weeks
        dates_daily = ["2025-01-17", "2025-01-18", "2025-01-19", "2025-01-21", "2025-01-22"]
        for date in dates_daily:
            add_event_habit(self.db, "daily_habit", date)

        dates_weekly = ["2024-12-16", "2024-12-23", "2024-12-30", "2025-01-06", "2025-01-13"]
        for date in dates_weekly:
            add_event_habit(self.db, "weekly_habit", date)

        dates_daily_2 = ["2025-01-16", "2025-01-17", "2025-01-20", "2025-01-23"]
        for date in dates_daily_2:
            add_event_habit(self.db, "daily_habit_2", date)

        dates_weekly_2 = ["2024-12-15", "2024-12-22", "2024-12-29", "2025-01-12"]
        for date in dates_weekly_2:
            add_event_habit(self.db, "weekly_habit_2", date)

    def test_habit_creation(self):
        # Test habit creation and adding events
        habit = Habit("test_habit_1", PeriodType.DAILY, creationDate="2025-01-17")
        habit.add_event(self.db, "2025-01-17")
        habit.add_event(self.db, "2025-01-18")

        habit_data = get_habit_data(self.db, "test_habit_1")
        assert len(habit_data) == 2  # Should have 2 events
        assert habit_data[0][0] == "2025-01-17"  # First event date check

    def test_db_counter(self):
        # Test database event count retrieval
        data = get_habit_data(self.db, "daily_habit")
        assert len(data) == 5  # 5 events added for daily_habit

        count = calculate_count(self.db, "daily_habit")
        assert count == 5  # Count should match the number of events

    def test_calculate_streak(self):
    # Load habit data
        habit = Habit("daily_habit", PeriodType.DAILY, creationDate="2025-01-17")
        habit.load_events(self.db)  # Ensure events are loaded

    # Calculate streaks
        current_streak, max_streak = calculate_streaks(habit)
        print(f"Events: {habit.events}")
        print(f"Current streak: {current_streak}, Max streak: {max_streak}")  # Debugging

        assert current_streak == 0  # Last 2 consecutive events
        assert max_streak == 3  # Maximum streak of 3 for daily_habit


        # Test streak calculation for weekly habit
        habit_weekly = Habit("weekly_habit", PeriodType.WEEKLY, creationDate="2024-12-16")
        current_streak, max_streak = calculate_streaks(habit_weekly)
        habit_weekly.load_events(self.db)
        print(f"Events for weekly_habit: {habit_weekly.events}")
        current_streak, max_streak = calculate_streaks(habit_weekly)
        print(f"Current streak for weekly_habit: {current_streak}, Max streak: {max_streak}")

        assert current_streak == 0  # Last week's event continues the streak
        assert max_streak == 1  # Maximum streak for weekly habit

    def test_get_longest_run_streak(self):
    # Test the get_longest_run_streak function with predefined habits and events

    # Calculate the longest run streak
        longest_streak_habit, longest_streak = get_longest_run_streak(self.db)

    # Debugging information
        print(f"Longest streak habit: {longest_streak_habit}, Longest streak: {longest_streak}")
    
    # Debugging information for loaded habits and events
        habits = Habit.load_all_habits(self.db)
        for habit in habits:
            print(f"Loaded habit: {habit.name}, Events: {habit.events}")

    # Validate the longest streak data (list comparison for habits with the same streak)
        assert sorted(longest_streak_habit) == sorted(["weekly_habit"])
        assert longest_streak == 5  # Maximum streak for daily_habit

    # Add more events to another habit
        weekly_habit.add_event(self.db, event_date = "2025-01-20")
        weekly_habit.add_event(self.db, event_date = "2025-01-27")

    # Recalculate the longest run streak
        longest_streak_habit, longest_streak = get_longest_run_streak(self.db)

    # Debugging information
        print(f"Updated longest streak habit: {longest_streak_habit}, Longest streak: {longest_streak}")

    # Validate the updated streak
        assert longest_streak_habit == ["weekly_habit"]  # Expect a list with 'weekly_habit' now
        assert longest_streak == 5    # Expect the streak to be 5 now
    
    def teardown_method(self):
        # Close the database connection and remove the test database
        if self.db:
            self.db.close()

        if os.path.exists("test.db"):
            os.remove("test.db")  # Clean up the test database after testing
'''