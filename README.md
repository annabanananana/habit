# My habit tracking App

This application was created using python and VSC. 
The user can create daily or weekly habits, increment them when the habit was carried out, and delete a habit if neccessary.
In the analyze part the user can look at the count of a habit, and at the current and maximum run streaks of a specific habit or of daily/weekly habits or overall habits. It also includes a test_project.py file which automatically tests the application.

## This is a habit tracking app for daily and weekly habits. You can use the app through the command line interface using the following commands:
  
  create:     
  Create a new habit
  increment:  
  Increment the habit's event count
  filter:     
  Filter and display habits by periodicity (DAILY or WEEKLY).
  show:       
  Show all habits
  analyze:    
  select from a the list:
  "List all habits",
  "List habits by periodicity",
  "Habit count",
  "Longest run streak (daily habits)",
  "Longest run streak (weekly habits)",
  "Longest run streak (specific habit)",
  "Longest run streak (overall)",
  "Show table of habits",
  "Back",
  exit-cli:   
  Exit the habit tracker CLI

## Installation

Be sure to have python installed on your computer.

download or clone the git repository.

in the coresponding directory run the following command to install necessary packages
pip install -requirements.txt

## Usage

Start the program with following command:

python main.py

this will show you the upper commands you can chose from. Start off with 'create' to add a new habit to your database

## Tests

pytest  .

You can adjust the test file with additional date, e.g., but be sure to update the assertions with it.

### I hope you enjoy my habti tracker app!