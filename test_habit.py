import unittest
from datetime import date
from db import get_db, habit_exists, get_habit_data
from habit import Habit, PeriodType


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

    def test_create_habit(self):
        """Test habit creation and retrieval from DB"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        self.assertTrue(habit_exists(self.db, habit_name))

    def test_increment_habit(self):
        """Test habit event increment"""
        habit_name = "Exercise"
        habit = Habit(habit_name, PeriodType.DAILY, date.today())
        habit.store(self.db)
        habit.add_event(self.db)
        events = get_habit_data(self.db, habit_name)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0][0], date.today().isoformat())


if __name__ == "__main__":
    unittest.main()
    # OR explicitly run the tests
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestHabitTracker))
