h = -1

while h < 1 or h > 8:
    height = input("Height: ")
    try:
        h = int(height)
    except ValueError:
        pass

for step in range(h):
    print(" " * (h - step - 1) + "#" * (step + 1))
