from cs50 import get_string

# Ask user for text
text = get_string("Text: ")

# Count The Number of Letters in Text
num_letters = len([c for c in text if c.isalpha()])

# Count The Number of Words in Text
num_words = 1 + len([c for c in text if c == " "])

# Count The Number of Sentences in Text
num_sentences = len([c for c in text if (c == "." or c == "!" or c == "?")])

# Calculate Coleman-Liau Index
L = num_letters / num_words * 100
S = num_sentences / num_words * 100
idx = int(round(0.0588 * L - 0.296 * S - 15.8, 0))

# Return the Score to the user
if idx >= 16:
    print("Grade 16+")
elif idx < 1:
    print("Before Grade 1")
else:
    print("Grade", idx)