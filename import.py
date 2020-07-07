'''
    Python script to import data from a csv file
    and create an SQLite database.
'''
# IMPORT LIBRARIES
import csv
import sys
import cs50

# CHECK CORRECT USAGE
if len(sys.argv[:]) != 2:
    print("ERROR -- Usage: python import.py characters.csv")
    pass

# CREATE A CONNECTION TO THE SQLITE DATABASE
FILE = open("students.db", "w")
db = cs50.SQL("sqlite:///students.db")

# CREAT TABLE CALLED 'students' IN THE SQL DATABASE FILE CALLED 'students.db'
db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth INT)")

# OPEN CSV FILE GIVEN BY COMMAND-LINE ARGUMENT
with open(sys.argv[1], "r") as characters:

    # READ THE CSV FILE AS A DICTIONARY
    reader = csv.DictReader(characters)

    # READ EACH ROW OF THE CSV
    for row in reader:

        # CHECK IF THE STUDENT HAS A MIDDLE NAME, IF NOT INSERT 'NONE'
        row["name"] = row["name"].split()
        if len(row["name"]) == 2:
            row["name"].insert(1, None)

        # ASSIGN VARIABLES FOR EACH COLUMN
        first = row["name"][0]
        middle = row["name"][1]
        last = row["name"][2]
        house = row["house"]
        birth = row["birth"]

        # INSERT EACH STUDENTS DETAILS INTO THE DATABASE
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", first, middle, last, house, birth)

# CLOSE THE .DB FILE
FILE.close()