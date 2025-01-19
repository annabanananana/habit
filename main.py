import click
import questionary
from db import get_db, add_counter
from habit import Habit, PeriodType
from analyze import calculate_count, calculate_streak
from datetime import datetime

# Store the current habit
current_habit = None

@click.group()
def cli():
    """Habit Tracker CLI"""
    global current_habit
    current_habit = None  # Reset current habit at the start

@click.command()
def create():
    """Create a new habit"""
    global current_habit

    habit_name = questionary.text("What is the name of your habit?").ask()
    if not habit_name:
        click.echo("Habit name cannot be empty.")
        return

    period_type = questionary.select(
        "What is the period type?",
        choices=["Daily", "Weekly"]
    ).ask()

    if not period_type:
        click.echo("You must select a period type.")
        return

    # Convert period_type to the appropriate enum
    period = PeriodType.DAILY if period_type == "Daily" else PeriodType.WEEKLY

    # Create and store the habit
    current_habit = Habit(habit_name, period, creationDate=datetime.today())
    current_habit.add_event(get_db())
    click.echo(f"Habit '{habit_name}' created successfully as a {period_type.lower()} habit.")


@click.command()
def increment():
    """Increment the habit's event count"""
    global current_habit
    if current_habit:
        current_habit.execution()
        current_habit.add_event(get_db())  # Log the event
        click.echo(f"Incremented {current_habit.name}!")
    else:
        click.echo("No habit created yet!")

@click.command()
def analyze():
    """Analyze the habit's execution data"""
    global current_habit
    if current_habit:
        count = calculate_count(get_db(), current_habit.name)
        streak = calculate_streak(get_db(), current_habit.name, current_habit.periodType.name)
        click.echo(f"{current_habit.name} has been incremented {count} times.")
        click.echo(f"The longest streak for {current_habit.name} is {streak} {current_habit.periodType.name.lower()}(s).")
    else:
        click.echo("No habit created yet!")

@click.command()
def exit_cli():
    """Exit the habit tracker CLI"""
    click.echo("Goodbye!")
    exit()

# Add the commands to the CLI group
cli.add_command(create)
cli.add_command(increment)
cli.add_command(analyze)
cli.add_command(exit_cli)

if __name__ == "__main__":
    cli()


'''
import questionary
from db import get_db
#from counter import Counter
from habit import Habit, PeriodType
from analyse import calculate_count
from datetime import datetime

def cli():
    db = get_db()
    questionary.confirm("are you ready?").ask()

    stop = False
    while not stop:
        choice = questionary.select(
        "What do you want to do?",
        choices=["Create", "Increment", "Analyse", "Exit"]
    ).ask()

        

        if choice == "Create":
            habitName = questionary.text("What is the name of your habit?").ask()
            habit = Habit(habitName, PeriodType.DAILY, creationDate=datetime.today())
            #habit.store(db)
        elif choice == "Increment":
            habit = Habit(habitName, "no description", creationDate = datetime.today())
            habit.execution()
            habit.add_event(db)
        elif choice == "Analyse":
            count = calculate_count(db, "")
            print(f"{habitName} has been incremented {count} times")
        else:
            print("Bye!")
            stop = True



if __name__ == "__main__":
    cli()

'''