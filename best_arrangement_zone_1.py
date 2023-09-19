from queue import Queue

from backdrop import Backdrop, Tile


if __name__ == "__main__":
    bdrop = Backdrop()
    # Auto placement
    bdrop.set_tile(0, 0, Tile("yellow"))
    bdrop.set_tile(0, 1, Tile("yellow"))

    # Other placements
    bdrop.set_tile(1, 1, Tile("yellow"))

    bdrop.set_tile(0, 2, Tile("white"))
    bdrop.set_tile(1, 2, Tile("white"))
    bdrop.set_tile(1, 0, Tile("white"))
    bdrop.set_tile(2, 0, Tile("white"))
    bdrop.set_tile(2, 1, Tile("white"))

    bdrop.set_tile(3, 0, Tile("purple"))
    bdrop.set_tile(3, 1, Tile("purple"))
    bdrop.set_tile(4, 0, Tile("purple"))

    bdrop.set_tile(0, 4, Tile("green"))
    bdrop.set_tile(0, 5, Tile("green"))
    bdrop.set_tile(1, 5, Tile("green"))

    bdrop.set_tile(0, 3, Tile("white"))
    bdrop.set_tile(1, 4, Tile("white"))

    bdrop.set_tile(1, 3, Tile("green"))
    bdrop.set_tile(2, 2, Tile("yellow"))
    bdrop.set_tile(2, 3, Tile("purple"))

    bdrop.set_tile(3, 2, Tile("white"))
    bdrop.set_tile(3, 3, Tile("white"))

    bdrop.set_tile(3, 3, Tile("white"))
    bdrop.set_tile(4, 1, Tile("white"))
    bdrop.set_tile(4, 2, Tile("white"))
    bdrop.set_tile(5, 0, Tile("white"))
    bdrop.set_tile(5, 1, Tile("white"))
    bdrop.set_tile(5, 2, Tile("white"))

    bdrop.set_tile(6, 0, Tile("green"))
    bdrop.set_tile(6, 1, Tile("purple"))
    bdrop.set_tile(7, 1, Tile("yellow"))

    bdrop.set_tile(7, 0, Tile("white"))
    bdrop.set_tile(8, 0, Tile("white"))


    bdrop.generate_legal_moves()
    print(bdrop.get_legal_moves())
    # bdrop.set_tile(0, 4, Tile("green"))
    print(bdrop)
    print("SCORE:", bdrop.calculate_score())
    print("White tiles",[x.identity() for x in bdrop.get_placed_tiles()].count('white'))
