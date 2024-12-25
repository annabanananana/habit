import questionary
from db import get_db
from counter import Counter
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
            habit = Habit(habitName, PeriodType.DAILY, creationDate=datetime.now())
            #counter.store(db)
        elif choice == "Increment":
            counter = Counter("", "no description")
            counter.increment()
            counter.add_event(db)
        elif choice == "Analyse":
            count = calculate_count(db, "")
            print(f" has been incremented {count} times")
        else:
            print("Bye!")
            stop = True



if __name__ == "__main__":
    cli()