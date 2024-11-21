def chess_input(s):
    while True:
        try:
            col, row = input(s).lower().strip()
            if 'a' <= col <= 'h' and 1 <= int(row) <= 8:
                return (f"{col}{row}")
            print("Input has to be 2 characters.\nLetter between A-H\nNumber between 1-8\n")
        except ValueError or TypeError:
            return True