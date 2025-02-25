'''
This code was generated with the help of ChatGPT. Following prompt was used:
I want to code a habit tracker app using python and using the CLI. I also want to use questionary and click for easier handling. 
Further more I want to be able to create, increment, and analyze my habits. 
There should be weekly and monthly habits, which I want to track if they are fullfilled or not. 
Throughout the programming ChatGPT was used to solve some other issues, like implementing the overview table and generating the test data.
'''

import click
import questionary
import sqlite3
from db import get_db
from habit import Habit, PeriodType
from analyze import calculate_count, calculate_streaks, get_habits_by_periodicity, get_longest_streak, get_longest_daily_run_streak, get_longest_weekly_run_streak
from datetime import datetime, date
from tabulate import tabulate

@click.group()
def cli():
    """Habit Tracker CLI"""
    global current_habit
    current_habit = None  # Reset current habit at the start

@cli.command()
def create():
    """Create a new habit"""
    try:
        habit_name = questionary.text("What is the name of your habit?").ask()
        period_type = questionary.select("What is the period type?", choices=["Daily", "Weekly"]).ask()
        period_type = PeriodType.DAILY if period_type == "Daily" else PeriodType.WEEKLY

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO habit (name, periodType) VALUES (?, ?)", (habit_name, period_type.value))
        db.commit()
        click.echo(f"Habit '{habit_name}' created successfully as a {'daily' if period_type == PeriodType.DAILY else 'weekly'} habit.")
    except sqlite3.IntegrityError as e:
        click.echo(f"Error creating habit: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")

@cli.command()
def increment():
    """Increment the habit's event count"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM habit")
        habits = cursor.fetchall()

        if not habits:
            click.echo("No habit created yet!")
            return

        habit_names = [name for name, in habits]
        selected_habit = questionary.select("Which habit do you want to increment?", choices=habit_names).ask()

        cursor.execute("SELECT * FROM habit WHERE name = ?", (selected_habit,))
        habit = cursor.fetchone()
        if not habit:
            click.echo(f"Habit '{selected_habit}' not found!")
            return

        cursor.execute("INSERT INTO tracker (date, habitName) VALUES (?, ?)", (date.today().isoformat(), selected_habit))
        db.commit()
        click.echo(f"Habit '{selected_habit}' has been incremented.")
    except sqlite3.Error as e:
        click.echo(f"Error interacting with the database: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")


@click.command("filter_habits")
@click.option("--period", type=click.Choice(["DAILY", "WEEKLY"], case_sensitive=False), prompt="Enter the period type (DAILY or WEEKLY)")
def filter_habits(period):
    """
    Filter and display habits by periodicity (DAILY or WEEKLY).
    """
    db = get_db()
    period_type = PeriodType.DAILY if period.upper() == "DAILY" else PeriodType.WEEKLY
    cur = db.cursor()
    cur.execute("SELECT name, periodType FROM habit WHERE periodType=?", (period_type.value,))
    habits = cur.fetchall()

    if habits:
        print(f"Habits with {period.upper()} periodicity:")
        for name, _ in habits:
            print(f"- {name}")
    else:
        print(f"No habits found with {period.upper()} periodicity.")

@click.command()
def analyze():
    """Analyze habit data."""
    db = get_db()

    # Ask the user which analysis they want to perform
    choice = questionary.select(
        "Which analysis would you like to perform?",
        choices=[
            "List all habits",
            "List habits by periodicity",
            "Habit count",#not yet included
            "Longest run streak (daily habits)",
            "Longest run streak (weekly habits)",
            "Longest run streak (specific habit)",
            "Back"
        ],
    ).ask()

    if choice == "List all habits":
        habits = Habit.load_all_habits(db)
        if habits:
            click.echo("Here are all your tracked habits:")
            for habit in habits:
                click.echo(f"- {habit.name} ({habit.period_type.name})")
        else:
            click.echo("No habits found.")

    elif choice == "List habits by periodicity":
        period_choice = questionary.select(
            "Which periodicity?",
            choices=["Daily", "Weekly"]
        ).ask()
        periodicity = PeriodType.DAILY if period_choice == "Daily" else PeriodType.WEEKLY
        habits = get_habits_by_periodicity(db, periodicity)
        if habits:
            click.echo(f"Habits with {period_choice.lower()} periodicity:")
            for habit in habits:
                click.echo(f"- {habit.name}")
        else:
            click.echo(f"No {period_choice.lower()} habits found.")
    
    elif choice == "Habit count":
        habits = Habit.load_all_habits(db)
        if not habits:
            click.echo("No habits found.")
            return

        habit_name = questionary.select(
            "Which habit?",
            choices=[habit.name for habit in habits]
        ).ask()
        count = calculate_count(db, habit_name)
        if count > 0:
            click.echo(f"The habit '{habit_name}' has been executed {count} times.")
        else:
            click.echo(f"The habit '{habit_name}' has not been executed yet.")

    elif choice == "Longest run streak (daily habits)":
        daily_habits = get_habits_by_periodicity(db, PeriodType.DAILY)
        if not daily_habits:
            click.echo("No daily habits found.")
            return

        longest_daily_habits = get_longest_daily_run_streak(db)
        if longest_daily_habits:
            habit_list = "\n".join([f"- {habit} ({streak} days)" for habit, streak in longest_daily_habits])
            click.echo(f"📅 **Daily habits with the longest streak:**\n{habit_list}")
        else:
            click.echo("No streaks available for daily habits.")

    elif choice == "Longest run streak (weekly habits)":
        weekly_habits = get_habits_by_periodicity(db, PeriodType.WEEKLY)
        if not weekly_habits:
            click.echo("No weekly habits found.")
            return
    
        longest_weekly_habits = get_longest_weekly_run_streak(db)
        if longest_weekly_habits:
            habit_list = "\n".join([f"- {habit} ({streak} weeks)" for habit, streak in longest_weekly_habits])
            click.echo(f"📅 **Weekly habits with the longest streak:**\n{habit_list}")
        else:
            click.echo("No weekly habits found or no streaks available.")

    elif choice == "Longest run streak (specific habit)":
        habits = Habit.load_all_habits(db)
        if not habits:
            click.echo("No habits found.")
            return

        habit_name = questionary.select(
            "Which habit?",
            choices=[habit.name for habit in habits]
        ).ask()

        habit = next(h for h in habits if h.name == habit_name)
        current_streak, max_streak = calculate_streaks(habit)
        click.echo(f"The habit '{habit.name}' has a current streak of {current_streak} days and a max streak of {max_streak} days.")

    elif choice == "Back":
        click.echo("Returning to main menu.")
'''
@cli.command()
def analyze():
    """Analyze the habit's execution data and show an overview"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name, periodType FROM habit")
        habits = cursor.fetchall()

        if not habits:
            click.echo("No habits found!")
            return

        table_data = []
        headers = ["Habit Name", "Period Type", "Total Count", "Current Streak", "Max Streak"]

        for name, period_type_value in habits:
            period_type = PeriodType(period_type_value)

            cursor.execute("SELECT date FROM tracker WHERE habitName = ?", (name,))
            events = [row[0] for row in cursor.fetchall()]

            habit = Habit(name, period_type, None)
            habit.events = events
            total_count = calculate_count(db, name)
            current_streak, max_streak = calculate_streaks(habit)

            table_data.append([name, "Weekly" if period_type == PeriodType.WEEKLY else "Daily", total_count, current_streak, max_streak])

        click.echo(tabulate(table_data, headers, tablefmt="grid"))
    except sqlite3.Error as e:
        click.echo(f"Error interacting with the database: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")

def analyze_all_habits():
    """
    Analyze all habits and show their current and maximum streaks.
    Also, display the habit with the longest streak overall.
    """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT name, periodType FROM habit")
    habits = cur.fetchall()

    if not habits:
        print("No habits found.")
        return

    print("Habit Analysis:")
    longest_streak_habit = None
    longest_streak = 0

    for name, periodType in habits:
        habit = Habit(name, PeriodType(periodType))
        habit.load_events(db)
        current_streak, max_streak = calculate_streaks(habit)
        print(f"- {habit.name}: Current Streak = {current_streak}, Max Streak = {max_streak}")

        if max_streak > longest_streak:
            longest_streak = max_streak
            longest_streak_habit = habit.name

    if longest_streak_habit:
        print(f"\nHabit with the longest streak: {longest_streak_habit} ({longest_streak} days)")

@click.command("analyze")
@click.argument("name", required=False)
def analyze_habit(name):
    """
    Analyze a single habit or all habits if no name is provided.
    """
    db = get_db()

    if name:
        cur = db.cursor()
        cur.execute("SELECT name, periodType FROM habit WHERE name=?", (name,))
        habit_data = cur.fetchone()

        if not habit_data:
            print(f"Habit '{name}' not found.")
            return

        habit = Habit(habit_data[0], PeriodType(habit_data[1]))
        habit.load_events(db)
        current_streak, max_streak = calculate_streaks(habit)
        print(f"Habit '{habit.name}': Current Streak = {current_streak}, Max Streak = {max_streak}")
    else:
        analyze_all_habits()
'''

@click.command()
def show_habits():
    """Show all habits"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, periodType FROM habit")
    habits = cursor.fetchall()

    if not habits:
        click.echo("No habits found.")
        return

    click.echo("Here are your current habits:")
    for name, period_type in habits:
        period_name = "Daily" if period_type.upper() == "DAILY" else "Weekly"
        click.echo(f"- {name}: {period_name}")


@click.command()
def exit_cli():
    """Exit the habit tracker CLI"""
    click.echo("Goodbye!")
    exit()

# Add the commands to the CLI group
cli.add_command(create)
cli.add_command(increment)
cli.add_command(analyze)
cli.add_command(show_habits)
cli.add_command(exit_cli)
cli.add_command(filter_habits)


if __name__ == "__main__":
    cli()
