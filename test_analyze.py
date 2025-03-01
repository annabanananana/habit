import sqlite3
import unittest
from datetime import date, timedelta
from db import get_db, add_event_habit, habit_exists, get_habit_data
from habit import Habit, PeriodType
from analyze import (
    calculate_count,
    calculate_streaks,
    get_habits_by_periodicity,
    get_longest_daily_run_streak,
    get_longest_weekly_run_streak,
)


class TestHabitTracker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests: sets up a new database."""
        cls.db = get_db(name="test_main.db")
        cls.db_cursor = cls.db.cursor()

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests: cleans up the test database."""
        cls.db_cursor.execute("DROP TABLE IF EXISTS habit")
        cls.db_cursor.execute("DROP TABLE IF EXISTS tracker")
        cls.db.commit()
        cls.db.close()

    def setUp(self):
        """Runs before each test: resets the database state."""
        self.db_cursor.execute("DELETE FROM habit")
        self.db_cursor.execute("DELETE FROM tracker")
        self.db.commit()

    def test_calculate_event_count(self):
        """Test event counting for a habit"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db, "2025-02-22")
        count = calculate_count(self.db, habit_name)
        self.assertEqual(count, 1)

    def test_calculate_event_count(self):
        """Test event counting for a habit"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db, "2025-02-22")
        count = calculate_count(self.db, habit_name)
        self.assertEqual(count, 1)

    def test_calculate_event_count(self):
        """Test event counting for a habit"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, "2025-02-22")
        count = calculate_count(self.db, habit_name)
        self.assertEqual(count, 2)

    def test_calculate_streaks_daily(self):
        """Test streak calculation for daily habits"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        current_streak, max_streak = calculate_streaks(habit)
        self.assertEqual(current_streak, 2)
        self.assertEqual(max_streak, 2)

    def test_calculate_streaks_weekly(self):
        """Test streak calculation for weekly habits"""
        habit_name = "Exercise"
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
        self.assertEqual(current_streak, 2)
        self.assertEqual(max_streak, 2)

    def test_get_habits_by_periodicity_daily(self):
        """Test filtering habits by daily periodicity"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        print(habit.name, habit.period_type)
        habits = get_habits_by_periodicity(self.db, PeriodType.DAILY)
        self.assertIn(habit.name, [h.name for h in habits])

    def test_get_habits_by_periodicity_weekly(self):
        """Test filtering habits by weekly periodicity"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        print(habit.name, habit.period_type)
        habits = get_habits_by_periodicity(self.db, PeriodType.WEEKLY)
        self.assertIn(habit.name, [h.name for h in habits])

    def test_longest_daily_streak(self):
        """Test calculation of longest daily streak"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(days=1)).isoformat())
        longest_daily = get_longest_daily_run_streak(self.db)
        self.assertIn((habit_name, 2), longest_daily)

    def test_longest_weekly_streak(self):
        """Test calculation of longest weekly streak"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.WEEKLY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        habit.add_event(self.db, (date.today() - timedelta(weeks=1)).isoformat())
        longest_weekly = get_longest_weekly_run_streak(self.db)
        self.assertIn((habit_name, 2), longest_weekly)

    def test_edge_case_no_habits(self):
        """Test behavior when no habits are created"""
        habits = get_habits_by_periodicity(self.db, PeriodType.DAILY)
        self.assertEqual(habits, [])

    def test_edge_case_no_events(self):
        """Test behavior when a habit has no events"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        current_streak, max_streak = calculate_streaks(habit)
        self.assertEqual(current_streak, 0)
        self.assertEqual(max_streak, 0)

    def test_edge_case_invalid_habit(self):
        """Test behavior when adding events to a non-existing habit"""
        with self.assertRaises(ValueError):
            add_event_habit(self.db, "NonExistentHabit")


if __name__ == "__main__":
    unittest.main()
    # OR explicitly run the tests
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestHabitTracker))
