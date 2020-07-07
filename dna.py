import sys
import csv


def main():
    '''
    The main function opens the csv & txt files,
    extracts the list of STRs to search for,
    and prints the name of the person whos dna profile matches the sample provided in the txt file.
    '''

    # If your program is executed with the incorrect number of command-line arguments, your program should print an error message of your choice (with print).
    if len(sys.argv[:]) != 3:
        print("USAGE: python dna.py databases/large.csv sequences/5.txt")
        return

    # Open people databse csv file and store in 'data'
    csv_data = open(sys.argv[1], 'r')

    # List of STRs to search for
    reader = csv.reader(csv_data)
    row1 = next(reader)
    list_of_str = row1[1:]

    # List of People
    list_of_people = [line for line in reader]

    # Open the dna file and store in 'dna'
    txt_data = open(sys.argv[2], 'r')
    dna = txt_data.read()

    # Locate the STR sequences in the dna sample provided
    str_sequences = findSTR(list_of_str, dna)

    # Find the person who matches the dna sample
    winner = findMatch(str_sequences, list_of_people)

    # Print the name of the winner
    print(winner)

    # Close the files
    csv_data.close()
    txt_data.close()
    return


def findSTR(list_of_str, dna):
    '''
    list_of_str: a list of strings that represent the STRs we are searching for.
    dna: a string of dna code.

    returns a list containing the longest consecutive sequence of each STR found within the dna sample
    '''

    # loc is a list of lists. 
    loc = []
    # Each inner list represents the locations of each instance of a single STR in the dna sample.
    for STR in list_of_str:
        # Store each STR location in a list
        STRlocs = [i for i in range(len(dna)) if dna[i: i + len(STR)] == STR]
        loc.append(STRlocs)

    # Make a list of the number of consecutive occurances of each STR
    seq = []
    for STRS in loc:
        sequences = []
        counter = 1
        for i in range(len(STRS) - 1):
            if (STRS[i + 1] - STRS[i]) == len(list_of_str[len(seq)]):
                counter += 1
            else:
                sequences.append(counter)
                counter = 1
        sequences.append(counter)
        seq.append(sequences)

    # Find the MAX sequence from each list
    max_seq = []
    for s in seq:
        max_seq.append(str(max(s)))

    return max_seq


def findMatch(str_sequences, list_of_people):
    '''
    str_sequences: a list of maximum consecutive sequences for each STR found in the dna sample
    list_of_people: a list of maximum consecutive sequences for each STR found in the that persons dna

    returns: the name of the person who is identical to the STR sequences found in the sampel.
    '''

    for person in list_of_people:
        if person[1:] == str_sequences:
            return(person[0])
    return("No Match")


# Execute main
main()