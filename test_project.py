import os
import pytest
from db import get_db, add_counter, execution_habit, get_habit_data
from habit import Habit, PeriodType
from analyze import calculate_count, calculate_streaks

class TestHabitTracker:

    def setup_method(self):
        # Setup the test database
        self.db = get_db("test.db")
        
        # Add sample habit data for testing
        add_counter(self.db, "test_habit", "Test habit description")
        execution_habit(self.db, "test_habit", "2021-12-06")
        execution_habit(self.db, "test_habit", "2021-12-07")
        execution_habit(self.db, "test_habit", "2021-12-09")
        execution_habit(self.db, "test_habit", "2021-12-10")
    
    def test_habit_creation(self):
        # Test habit creation and event counting
        habit = Habit("test_habit_1", PeriodType.DAILY, creationDate="2021-12-06")
        habit.add_event(self.db, "2021-12-06")
        habit.add_event(self.db, "2021-12-07")
        
        habit_data = get_habit_data(self.db, "test_habit_1")
        assert len(habit_data) == 2  # Should have 2 events
        assert habit_data[0][0] == "2021-12-06"  # Check if the first event is correct

    def test_db_counter(self):
        # Test database retrieval and count calculation
        data = get_habit_data(self.db, "test_habit")
        assert len(data) == 4  # Check if we have 4 events stored in the DB
        
        count = calculate_count(self.db, "test_habit")
        assert count == 4  # The count of events should be 4

    def test_calculate_streak(self):
        # Test the streak calculation function
        habit = Habit("test_habit_2", PeriodType.DAILY, creationDate="2021-12-06")
        habit.add_event(self.db, "2021-12-06")
        habit.add_event(self.db, "2021-12-07")
        habit.add_event(self.db, "2021-12-08")
        habit.add_event(self.db, "2021-12-11")
        
        current_streak, max_streak = calculate_streaks(habit)
        assert current_streak == 1  # As the events are consecutive, streak should be 3
        assert max_streak == 3  # Max streak should also be 3 for this example

    def teardown_method(self):
        # Close the database connection and remove the test database
        if self.db:
            self.db.close()
        
        if os.path.exists("test.db"):
            os.remove("test.db")  # Clean up the test database after testing

'''

from counter import Counter
from db import get_db, add_counter, increment_counter, get_counter_data
from analyze import calculate_count


class TestCounter:

    def setup_method(self):
        self.db = get_db("test.db")

        add_counter(self.db, "test_counter", "test_description")
        increment_counter(self.db, "test_counter", "2021-12-06")
        increment_counter(self.db, "test_counter", "2021-12-07")

        increment_counter(self.db, "test_counter", "2021-12-09")
        increment_counter(self.db, "test_counter", "2021-12-10")


    def test_counter(self):
        counter = Counter("test_counter_1", "test_description_1")
        counter.store(self.db)

        counter.increment()
        counter.add_event(self.db)
        counter.reset()
        counter.increment()

    def test_db_counter(self):
        data = get_counter_data(self.db, "test_counter")
        assert len(data) == 4

        count = calculate_count(self.db, "test_counter")
        assert count == 4

    def teardown_method(self):
        import os
        os.remove("test.db")

    #used chatgpt to resolve issue with test.db; encountered permission error
    def teardown_method(self):
        import os
    # Close the database connection
        if self.db:
            self.db.close()
    # Remove the test database file
        os.remove("test.db")
'''