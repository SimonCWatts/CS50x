
# Ask user for an input between 1 - 8
h = -1
while h < 1 or h > 8:
    height = input("Height: ")
    try:
        h = int(height)
    except ValueError:
        pass

# Print Pyramid
for step in range(1, h + 1):
    print(" " * (h - step) + "#" * (step) + "  " + "#" * (step))

