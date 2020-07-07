from cs50 import get_string

# Ask user for card number
card = get_string("Number: ")

# American Express uses 15-digit numbers,
# All American Express numbers start with 34 or 37
if len(card) == 15 and (card[0:2] == '34' or card[0:2] == '37'):
    print("AMEX\n")

# Visa uses 13- and 16-digit numbers
# All Visa numbers start with 4.
elif card[0] == '4' and (len(card) == 13 or len(card) == 16):
    print("VISA\n")

# MasterCard uses 16-digit numbers, and
# Most MasterCard numbers start with 51, 52, 53, 54, or 55
elif len(card) == 16 and (card[0:2] == '51' or card[0:2] == '52' or card[0:2] == '53' or card[0:2] == '54' or card[0:2] == '55'):
    print("MASTERCARD\n")
    
# Input is INVALID
else:
    print("INVALID\n")