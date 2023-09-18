class Position:
    def __init__(self, row, col):
        if row > 11:
            raise ValueError("Row must be between 0 and 11")
        if col > 6:
            raise ValueError("Column must be between 0 and 6")
        if row % 2 == 0 and col > 5:
            raise ValueError("Column must be between 0 and 5 for even rows")
        if row % 2 == 1 and col > 6:
            raise ValueError("Column must be between 0 and 6 for odd rows")

        self.__row = row
        self.__col = col

    def row(self):
        return self.__row

    def col(self):
        return self.__col
