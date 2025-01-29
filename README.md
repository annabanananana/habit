# My habit tracking App

Description

##This is a habit tracking app for daily and weekly habits. You can use the app through the command line interface using the following commands:
  analyze    Analyze the habit's execution data and show an overview
  create     Create a new habit
  exit-cli   Exit the habit tracker CLI
  filter     Filter and display habits by periodicity (DAILY or WEEKLY).
  increment  Increment the habit's event count
  show       Show all habits

It also includes a test_project.py file which automatically tests the application.

##Installation

download or clone the git repository.

'''shell
in the coresponding directory run the following command to install necessary packages
pip install -requirements.txt '''

##Usage

Start the program with following command:

'''shell
python main.py '''

this will show you the upper commands you can chose from. Start off with 'create' to add a new habit to your database
##tests
to run the test file, go to the db.py file line 6 and change name="main.db" into name="test.db" and run the following command

'''shell
pytest  .
'''

you can adjust the test file with additional date, e.g., but be sure to update the assertions with it.
