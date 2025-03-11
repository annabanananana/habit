import os
from datetime import date, timedelta
from db import get_db, add_event_habit, get_habit_data
from habit import Habit, PeriodType
from analyze import (
    calculate_count,
    calculate_streaks,
    get_habits_by_periodicity,
    get_longest_daily_run_streak,
    get_longest_weekly_run_streak,
    get_longest_overall_run_streak,
)
import pytest


class TestHabitTracker:

    TEMP_TEST_DB = "test_main.db"

    @classmethod
    def setup_class(cls):
        """Runs once before all tests: sets up a new database."""
        cls.db = get_db(cls.TEMP_TEST_DB)
        cls.db_cursor = cls.db.cursor()

    def setup_method(self):
        """Runs before each test: resets the database state."""
        self.db_cursor.execute("DELETE FROM habit")
        self.db_cursor.execute("DELETE FROM tracker")
        self.db.commit()

    @classmethod
    def teardown_class(cls):
        """Runs once after all tests: cleans up the test database."""
        cls.db_cursor.execute("DROP TABLE IF EXISTS habit")
        cls.db_cursor.execute("DROP TABLE IF EXISTS tracker")
        cls.db.commit()
        cls.db.close()
        os.remove(cls.TEMP_TEST_DB)

    def test_calculate_event_count(self):
        """Test event counting for a habit"""
        habit_name = "Exercise_daily1"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db, "2025-02-22")
        # count = calculate_count(self.db, habit_name)
        # assert count == 1
        habit.add_event(self.db, "2025-02-23")
        habit.add_event(self.db, "2025-02-24")
        habit.add_event(self.db, "2025-02-25")
        habit.add_event(self.db, "2025-02-27")
        count = calculate_count(self.db, habit_name)
        assert count == 5

    def test_calculate_event_count(self):
        """Test event counting for a daily habit"""
        habit_name = "Exercise_daily2"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, "2025-02-22")
        count = calculate_count(self.db, habit_name)
        assert count == 2

    def test_calculate_event_count(self):
        """Test event counting for a weekly habit"""
        habit_name = "Exercise_weekly1"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, "2025-02-15")
        habit.add_event(self.db, "2025-02-18")
        habit.add_event(self.db, "2025-02-22")
        count = calculate_count(self.db, habit_name)
        assert count == 4

    def test_calculate_streaks_daily(self):
        """Test streak calculation for daily habits"""
        habit_name = "Exercise_daily3"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        current_streak, max_streak = calculate_streaks(habit)
        assert current_streak == 2
        assert max_streak == 2

    def test_calculate_streaks_daily(self):
        """Test streak calculation for daily habits"""
        habit_name = "Exercise_daily4"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=2)).isoformat())
        habit.add_event(self.db, "2025-02-22")
        habit.add_event(self.db, "2025-02-23")
        habit.add_event(self.db, "2025-02-24")
        habit.add_event(self.db, "2025-02-25")
        habit.add_event(self.db, "2025-02-26")
        current_streak, max_streak = calculate_streaks(habit)
        assert current_streak == 3
        assert max_streak == 5

    def test_calculate_streaks_weekly(self):
        """Test streak calculation for weekly habits"""
        habit_name = "Exercise_weekly3"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)

        # Add events with a 7-day gap
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=7)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=14)).isoformat())
        habit.add_event(self.db, "2024-12-16")
        habit.add_event(self.db, "2024-12-23")
        habit.add_event(self.db, "2024-12-30")
        habit.add_event(self.db, "2025-01-06")
        habit.add_event(self.db, "2025-01-13")

        # Debugging: Check if events are correctly added
        events = get_habit_data(self.db, habit_name)
        print(f"Stored events: {events}")

        # Calculate streaks
        current_streak, max_streak = calculate_streaks(habit)

        # Debugging: Print out calculated streaks
        print(f"Calculated streaks: Current - {current_streak}, Max - {max_streak}")

        # Assert the correct streak values
        assert current_streak == 3
        assert max_streak == 5

    def test_calculate_streaks_weekly(self):
        """Test streak calculation for weekly habits"""
        habit_name = "Exercise_weekly2"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)

        # Add events with a 7-day gap
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=7)).isoformat())

        # Debugging: Check if events are correctly added
        events = get_habit_data(self.db, habit_name)
        print(f"Stored events: {events}")

        # Calculate streaks
        current_streak, max_streak = calculate_streaks(habit)

        # Debugging: Print out calculated streaks
        print(f"Calculated streaks: Current - {current_streak}, Max - {max_streak}")

        # Assert the correct streak values
        assert current_streak == 2
        assert max_streak == 2

    def test_get_habits_by_periodicity_daily(self):
        """Test filtering habits by daily periodicity"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        print(habit.name, habit.period_type)
        habits = get_habits_by_periodicity(self.db, PeriodType.DAILY)
        assert habit_name in [h.name for h in habits]

    def test_get_habits_by_periodicity_weekly(self):
        """Test filtering habits by weekly periodicity"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        print(habit.name, habit.period_type)
        habits = get_habits_by_periodicity(self.db, PeriodType.WEEKLY)
        assert habit_name in [h.name for h in habits]

    def test_longest_daily_streak(self):
        """Test calculation of longest daily streak"""
        habit_name = "Exercise_daily1"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        habit_name = "Exercise_daily2"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=2)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=3)).isoformat())
        longest_daily = get_longest_daily_run_streak(self.db)
        assert longest_daily == [(habit_name, 4)]

    def test_longest_weekly_streak(self):
        """Test calculation of longest weekly streak"""
        habit_name = "Exercise_weekly1"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(weeks=1)).isoformat())
        habit_name = "Exercise_weekly2"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(weeks=1)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=2)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=3)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=4)).isoformat())
        longest_weekly = get_longest_weekly_run_streak(self.db)
        assert longest_weekly == [(habit_name, 5)]

    def test_longest_daily_streak_tie(self):
        """Test calculation of longest daily streak with a tie"""
        habit_name = "Exercise_daily1"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        habit_name = "Exercise_daily2"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        longest_daily = get_longest_daily_run_streak(self.db)
        assert longest_daily == [("Exercise_daily1", 2), ("Exercise_daily2", 2)]

    def test_longest_weekly_streak_tie(self):
        """Test calculation of longest weekly streak with a tie"""
        habit_name = "Exercise_weekly1"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(weeks=1)).isoformat())
        habit_name = "Exercise_weekly2"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(weeks=1)).isoformat())
        longest_weekly = get_longest_weekly_run_streak(self.db)
        assert longest_weekly == [("Exercise_weekly1", 2), ("Exercise_weekly2", 2)]

    def test_get_longest_overall_streak(self):
        """Test calculation of longest overall streak"""
        habit_name = "Exercise_daily1"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=2)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=3)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=4)).isoformat())
        habit_name = "Exercise_weekly1"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(weeks=1)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=2)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=3)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=4)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=5)).isoformat())
        longest_overall = get_longest_overall_run_streak(self.db)
        assert longest_overall == [(habit_name, 6)]

    def test_get_longest_overall_streak_tie(self):
        """Test calculation of longest overall streak"""
        habit_name = "Exercise_daily1"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=2)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=3)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=4)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(days=5)).isoformat())
        habit_name = "Exercise_weekly1"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(weeks=1)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=2)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=3)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=4)).isoformat())
        habit.add_event(self.db, (date.today() - timedelta(weeks=5)).isoformat())
        longest_overall = get_longest_overall_run_streak(self.db)
        assert longest_overall == [("Exercise_daily1", 6), ("Exercise_weekly1", 6)]

    def test_edge_case_no_habits(self):
        """Test behavior when no habits are created"""
        habits = get_habits_by_periodicity(self.db, PeriodType.DAILY)
        assert not habits

    def test_edge_case_no_events(self):
        """Test behavior when a habit has no events"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        current_streak, max_streak = calculate_streaks(habit)
        assert current_streak == 0
        assert max_streak == 0

    def test_edge_case_invalid_habit(self):
        """Test behavior when adding events to a non-existing habit"""
        with pytest.raises(ValueError):
            add_event_habit(self.db, "NonExistentHabit")


if __name__ == "__main__":
    options = [__file__, "-v"]
    pytest.main(options)
