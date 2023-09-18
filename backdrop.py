class Tile:
    def __init__(self, color: str = None):
        self.__identity = color

    def identity(self):
        return self.__identity

    def __str__(self):
        if not self.__identity:
            return "\u2B21"  # Default to a white hexagon (change this character if needed)
        colors = {
            "white": "\x1b[97m\u2B22\x1b[0m",  # White hexagon with white foreground color
            "yellow": "\x1b[93m\u2B22\x1b[0m",  # White hexagon with yellow foreground color
            "purple": "\x1b[95m\u2B22\x1b[0m",  # White hexagon with purple foreground color
            "green": "\x1b[92m\u2B22\x1b[0m",  # White hexagon with green foreground color
        }
        return colors.get(self.__identity, "")  # Default to white hexagon


class Backdrop:
    def __init__(self):
        self.__backdrop: list[list[Tile]] = []
        for row in range(12):
            self.__backdrop.append([])
            for col in range(6 if row % 2 == 0 else 7):
                self.__backdrop[row].append(Tile(None))

        self.__legal_moves = []  # Starting row's legal moves

    def check_in_bounds(self, row, col):
        if row > 11:
            raise ValueError("Row must be between 0 and 11")
        if col > 6:
            raise ValueError("Column must be between 0 and 6")
        if row % 2 == 0 and col > 5:
            raise ValueError("Column must be between 0 and 5 for even rows")
        if row % 2 == 1 and col > 6:
            raise ValueError("Column must be between 0 and 6 for odd rows")

    def is_valid_mosaic_tile(self, row, col):
        self.check_in_bounds(row, col)
        return self.__backdrop[row][col].identity() is not None and self.__backdrop[row][col].identity() != "white"

    def score_backdrop(self):
        score = 0
        height_bonuses = [False, False, False]
        for row in range(12):
            for col in range(6 if row % 2 == 0 else 7):
                if not self.__backdrop[row][col].identity():
                    continue

                score += 5  # 5 Points for scoring a pixel (tile)

                # Add in height bonus checks here
                if row >= 2:
                    height_bonuses[0] = True
                if row >= 5:
                    height_bonuses[1] = True
                if row >= 8:
                    height_bonuses[2] = True

                # Now time for the hard part. Checking for mosaics.
                # So mosics are 3 hexagon tiles, in a triangle-ish shape, all adjacent to each other.
                # There are only 2 types of mosaics: 3 of the same color OR 3 different colors

                if row % 2 == 0:
                    if (self.is_valid_mosaic_tile(row, col) and self.is_valid_mosaic_tile(row - 1, col)
                            and self.is_valid_mosaic_tile(row - 1, col + 1)):
                        # Now to check if the mosaic is 3 of the same color or 3 different colors
                        tile_a = self.get_tile(row, col).identity()
                        tile_b = self.get_tile(row - 1, col).identity()
                        tile_c = self.get_tile(row - 1, col + 1).identity()
                    else:
                        # Not valid tiles so won't even bother
                        continue

                else:
                    if col == 0 or col == 6:
                        continue
                    if (self.is_valid_mosaic_tile(row, col) and self.is_valid_mosaic_tile(row - 1, col)
                            and self.is_valid_mosaic_tile(row - 1, col - 1)):
                        tile_a = self.get_tile(row, col).identity()
                        tile_b = self.get_tile(row - 1, col).identity()
                        tile_c = self.get_tile(row - 1, col + 1).identity()

                    else:
                        continue

                if not (tile_a == tile_b == tile_c or tile_a != tile_b != tile_c != tile_a):
                    continue

                # The mosaic might be valid, but we need to check if the borders are all white!
                acceptable_edges = ["white", "board", None]
                border_identites = [
                    self.get_tile(row, col + 1).identity() in acceptable_edges,
                    self.get_tile(row - 1, col + 2).identity() in acceptable_edges,
                    self.get_tile(row - 2, col + 1).identity() in acceptable_edges,

                    self.get_tile(row - 2, col).identity() in acceptable_edges,
                    self.get_tile(row - 2, col - 1).identity() in acceptable_edges,
                    self.get_tile(row - 1, col - 2).identity() in acceptable_edges,

                    self.get_tile(row, col - 1).identity() in acceptable_edges,
                    self.get_tile(row + 1, col).identity() in acceptable_edges,
                    self.get_tile(row + 1, col + 1).identity() in acceptable_edges,
                ]

                if not (False in border_identites):
                    # Edges are good = proper mosaic
                    print(f"Mosaic found at ({row}, {col})!")
                    score += 10
                if self.__backdrop[row][col].identity() == self.__backdrop[row][col + 1].identity() == \
                        self.__backdrop[row + 1][col].identity():
                    score += 10

        for bonus in height_bonuses:
            if bonus:
                score += 10

        return score

    def get_tile(self, row, col) -> Tile:
        # Same as using indices but returns none if out of bounds
        if row < 0 or row > 11:
            return Tile(None)
        if row % 2 == 0 and col < 0 or col > 5:
            return Tile(None)
        if row % 2 == 1 and col < 0 or col > 6:
            return Tile(None)
        return self.__backdrop[row][col]

    def is_legal_move(self, row, col):
        self.check_in_bounds(row, col)

        # Check if the tile is already occupied
        if self.__backdrop[row][col].identity():
            return False

        # Check there's two tiles below
        if row % 2 != 0:  # Odd row
            tile_left = self.__backdrop[row - 1][col - 1] if col > 0 else Tile("board")
            tile_right = self.__backdrop[row - 1][col] if col < 6 else Tile("board")

            if not (tile_left.identity() and tile_right.identity()):
                return False
        else:  # Even row (starts at 0)
            if row != 0:  # Row at 0 will always be supported
                # These never will be partially on top of the backdrop
                tile_left = self.__backdrop[row - 1][col]
                tile_right = self.__backdrop[row - 1][col + 1]

                if not (tile_left.identity() and tile_right.identity()):
                    return False

        # Check to make sure there's an opening above
        if self.__backdrop[row][col]:
            if row == 11:
                return True
            if row % 2 == 0:
                if not self.__backdrop[row + 1][col].identity() and not self.__backdrop[row + 1][col + 1].identity():
                    return True
            else:
                # The edge is being represented as Nones because I think it's possible to squeeze in a tile on the edge
                left_above = self.__backdrop[row + 1][col - 1] if col > 0 else Tile(None)
                right_above = self.__backdrop[row + 1][col] if col < 6 else Tile(None)

                if not left_above.identity() and not right_above.identity():
                    return True
        return False

    def set_tile(self, row, col, tile: Tile):
        if self.is_legal_move(row, col):
            self.__backdrop[row][col] = tile
            return True
        return False

    def get_tile(self, row, col):
        self.check_in_bounds(row, col)
        return self.__backdrop[row][col]

    def generate_legal_moves(self):
        self.__legal_moves.clear()
        for row in range(12):
            for col in range(6 if row % 2 == 0 else 7):
                if self.is_legal_move(row, col):
                    self.__legal_moves.append((row, col))

    def get_legal_moves(self):
        return self.__legal_moves

    def __str__(self):
        ret_str = "#" * 13 + "\n"
        # returns the backdrop in a nice format in text UI, given the 6/7 width alternating rows
        for n in range(len(self.__backdrop) - 1, -1, -1):
            if n % 2 == 0:
                ret_str += (
                    f" {self.__backdrop[n][0]} {self.__backdrop[n][1]} {self.__backdrop[n][2]} {self.__backdrop[n][3]} {self.__backdrop[n][4]} {self.__backdrop[n][5]}\n")
            else:
                ret_str += (
                    f"{self.__backdrop[n][0]} {self.__backdrop[n][1]} {self.__backdrop[n][2]} {self.__backdrop[n][3]} {self.__backdrop[n][4]} {self.__backdrop[n][5]} {self.__backdrop[n][6]}\n")
        ret_str += "#" * 13
        return ret_str
