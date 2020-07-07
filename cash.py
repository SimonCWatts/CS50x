from cs50 import get_float

# Prompt User for non-negative input
money = get_float("Change owed: ")
while not money > 0:
    money = get_float("Change owed: ")

# Dictionary: keys are coin values, values are the number of those coins required to provide change
change = {0.25: 0, 0.1: 0, 0.05: 0, 0.01: 0}

# For each coin in decending value order, decrement until negative, counting each time.
for coin in sorted(change, reverse=True):
    while money - coin >= 0.0:
        money = round(money - coin, 2)
        change[coin] += 1

# Print the total number of coins provided as change
print(sum(v for v in change.values()))