import questionary
from db import get_db
from counter import Counter
from analyse import calculate_count

def cli():
    db = get_db()
    questionary.confirm("are you read?").ask()

    stop = False
    while not stop:
        choice = questionary.select(
        "What do you want to do?",
        choices=["Create", "Increment", "Analyse", "Exit"]
    ).ask()

        name = questionary.text("What is the name of your counter?").ask()

        if choice == "Create":
            desc = questionary.text("What is the description of your counter?").ask()
            counter = Counter(name, desc)
            counter.store(db)
        elif choice == "Increment":
            counter = Counter(name, "no description")
            counter.increment()
            counter.add_event(db)
        elif choice == "Analyse":
            count = calculate_count(db, name)
            print(f"{name} has been incremented {count} times")
        else:
            print("Bye!")
            stop = True



if __name__ == "__main__":
    cli()