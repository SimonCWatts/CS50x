'''
    Reads data from the sqlite database 'students.db'
    and prints a list of students for a given house in alphabetical order.
'''

import csv
import sys
from cs50 import SQL

# ENSURE CORRECT USAGE
if len(sys.argv[:]) != 2:
    print("ERROR - USAGE: python roster.py Gryffindor")
    pass

# CREATE A CONNECTION TO THE SQLITE DATABASE
db = SQL("sqlite:///students.db")

# QUERY DATABASE FOR ALL STUDENTS IN THE SPECIFIED HOUSE
query = "SELECT first, middle, last, birth FROM students WHERE house = '" + sys.argv[1] + "' ORDER BY last, first;"
students = db.execute(query)

# PRINT EACH STUDENTS FULL NAME AND BIRTH YEAR
for student in students:
    if student['middle'] == None:
        print(student['first'], student['last'] + ", born", student['birth'])
    else:
        print(student['first'], student['middle'], student['last'] + ", born", student['birth'])