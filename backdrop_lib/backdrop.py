class Pixel:
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
        self.__backdrop: list[list[Pixel]] = []
        for row in range(12):
            self.__backdrop.append([])
            for col in range(6 if row % 2 == 0 else 7):
                self.__backdrop[row].append(Pixel(None))

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

    def is_valid_mosaic_pixel(self, row, col):
        self.check_in_bounds(row, col)
        return self.__backdrop[row][col].identity() is not None and self.__backdrop[row][col].identity() != "white"

    def calculate_score(self, verbose=False):
        score = 0
        height_bonuses = [False, False, False]
        for row in range(12):
            for col in range(6 if row % 2 == 0 else 7):
                if not self.__backdrop[row][col].identity():
                    continue

                score += 5  # 5 Points for scoring a pixel (pixel)

                # Add in height bonus checks here
                if row >= 2:
                    height_bonuses[0] = True
                if row >= 5:
                    height_bonuses[1] = True
                if row >= 8:
                    height_bonuses[2] = True

                # Now time for the hard part. Checking for mosaics.
                # So mosics are 3 hexagon pixels, in a triangle-ish shape, all adjacent to each other.
                # There are only 2 types of mosaics: 3 of the same color OR 3 different colors

                if row % 2 == 0:
                    if (self.is_valid_mosaic_pixel(row, col) and self.is_valid_mosaic_pixel(row - 1, col)
                            and self.is_valid_mosaic_pixel(row - 1, col + 1)):
                        # Now to check if the mosaic is 3 of the same color or 3 different colors
                        pixel_a = self.get_pixel(row, col).identity()
                        pixel_b = self.get_pixel(row - 1, col).identity()
                        pixel_c = self.get_pixel(row - 1, col + 1).identity()
                    else:
                        # Not valid pixels so won't even bother
                        continue

                else:
                    if col == 0 or col == 6:
                        continue
                    if (self.is_valid_mosaic_pixel(row, col) and self.is_valid_mosaic_pixel(row - 1, col)
                            and self.is_valid_mosaic_pixel(row - 1, col - 1)):
                        pixel_a = self.get_pixel(row, col).identity()
                        pixel_b = self.get_pixel(row - 1, col).identity()
                        pixel_c = self.get_pixel(row - 1, col + 1).identity()

                    else:
                        continue

                if not (pixel_a == pixel_b == pixel_c or pixel_a != pixel_b != pixel_c != pixel_a):
                    continue

                # The mosaic might be valid, but we need to check if the borders are all white!
                acceptable_edges = ["white", "board", None]
                border_identites = [
                    self.get_pixel(row, col + 1).identity() in acceptable_edges,
                    self.get_pixel(row - 1, col + 2).identity() in acceptable_edges,
                    self.get_pixel(row - 2, col + 1).identity() in acceptable_edges,

                    self.get_pixel(row - 2, col).identity() in acceptable_edges,
                    self.get_pixel(row - 2, col - 1).identity() in acceptable_edges,
                    self.get_pixel(row - 1, col - 2).identity() in acceptable_edges,

                    self.get_pixel(row, col - 1).identity() in acceptable_edges,
                    self.get_pixel(row + 1, col).identity() in acceptable_edges,
                    self.get_pixel(row + 1, col + 1).identity() in acceptable_edges,
                ]

                if not (False in border_identites):
                    # Edges are good = proper mosaic
                    if verbose:
                        print(f"Mosaic found at ({row}, {col})!")
                    score += 10
                if self.__backdrop[row][col].identity() == self.get_pixel(row, col + 1).identity() == \
                        self.__backdrop[row + 1][col].identity():
                    score += 10

        for bonus in height_bonuses:
            if bonus:
                score += 10

        return score

    def get_pixel(self, row, col) -> Pixel:
        # Same as using indices but returns none if out of bounds
        if row < 0 or row > 11:
            return Pixel(None)
        if row % 2 == 0 and col < 0 or col > 5:
            return Pixel(None)
        if row % 2 == 1 and col < 0 or col > 6:
            return Pixel(None)
        return self.__backdrop[row][col]

    def is_legal_move(self, row, col):
        self.check_in_bounds(row, col)

        # Check if the pixel is already occupied
        if self.__backdrop[row][col].identity():
            return False

        # Check there's two pixels below
        if row % 2 != 0:  # Odd row
            pixel_left = self.__backdrop[row - 1][col - 1] if col > 0 else Pixel("board")
            pixel_right = self.__backdrop[row - 1][col] if col < 6 else Pixel("board")

            if not (pixel_left.identity() and pixel_right.identity()):
                return False
        else:  # Even row (starts at 0)
            if row != 0:  # Row at 0 will always be supported
                # These never will be partially on top of the backdrop
                pixel_left = self.__backdrop[row - 1][col]
                pixel_right = self.__backdrop[row - 1][col + 1]

                if not (pixel_left.identity() and pixel_right.identity()):
                    return False

        # Check to make sure there's an opening above
        if self.__backdrop[row][col]:
            if row == 11:
                return True
            if row % 2 == 0:
                if not self.__backdrop[row + 1][col].identity() and not self.__backdrop[row + 1][col + 1].identity():
                    return True
            else:
                # The edge is being represented as Nones because I think it's possible to squeeze in a pixel on the edge
                left_above = self.__backdrop[row + 1][col - 1] if col > 0 else Pixel(None)
                right_above = self.__backdrop[row + 1][col] if col < 6 else Pixel(None)

                if not left_above.identity() and not right_above.identity():
                    return True
        return False

    def set_pixel(self, row, col, pixel: Pixel):
        if self.is_legal_move(row, col):
            self.__backdrop[row][col] = pixel
            return True
        return False

    def get_pixel(self, row, col):
        # self.check_in_bounds(row, col)
        try:
            return self.__backdrop[row][col]
        except:
            return Pixel(None)

    def generate_legal_moves(self):
        self.__legal_moves.clear()
        for row in range(12):
            for col in range(6 if row % 2 == 0 else 7):
                if self.is_legal_move(row, col):
                    self.__legal_moves.append((row, col))
        return self.__legal_moves

    def get_legal_moves(self):
        return self.__legal_moves

    def get_state(self):
        state = []
        color_to_id = {
            "white": 0,
            "yellow": 1,
            "purple": 2,
            "green": 3,
        }

        for row in range(12):
            for col in range(6 if row % 2 == 0 else 7):
                pixel = self.get_pixel(row, col)
                if pixel.identity() is not None:
                    pixel_id = color_to_id.get(pixel.identity(), -1)  # Assign a unique ID to each color
                    state.append(pixel_id)
                else:
                    # Handle the case where pixel.identity() is None (e.g., empty pixels)
                    state.append(-1)  # You can use -1 to represent empty pixels

        return state

    def __str__(self):
        ret_str = "#" * 15 + "\n"
        # returns the backdrop in a nice format in text UI, given the 6/7 width alternating rows
        for n in range(len(self.__backdrop) - 1, -1, -1):
            if n % 2 == 0:
                ret_str += (
                    f" {self.__backdrop[n][0]} {self.__backdrop[n][1]} {self.__backdrop[n][2]} {self.__backdrop[n][3]} {self.__backdrop[n][4]} {self.__backdrop[n][5]}\n")
            else:
                ret_str += (
                    f"{self.__backdrop[n][0]} {self.__backdrop[n][1]} {self.__backdrop[n][2]} {self.__backdrop[n][3]} {self.__backdrop[n][4]} {self.__backdrop[n][5]} {self.__backdrop[n][6]}\n")
        ret_str += "#" * 14
        return ret_str

    def get_num_placed_pixels(self):
        placed_pixels = 0
        for row in range(12):
            for col in range(6 if row % 2 == 0 else 7):
                if self.get_pixel(row, col).identity() is not None:
                    placed_pixels += 1
        return placed_pixels

    def get_placed_pixels(self):
        placed_pixels = []
        for row in range(12):
            for col in range(6 if row % 2 == 0 else 7):
                if self.get_pixel(row, col).identity() is not None:
                    placed_pixels.append(self.get_pixel(row, col))
        return placed_pixels
