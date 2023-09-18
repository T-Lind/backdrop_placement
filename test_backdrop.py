from backdrop import Backdrop, Tile

if __name__ == "__main__":
    bdrop = Backdrop()
    bdrop.set_tile(0, 0, Tile("yellow"))
    bdrop.set_tile(0, 1, Tile("purple"))
    bdrop.set_tile(1, 1, Tile("green"))
    bdrop.set_tile(1, 0, Tile("white"))
    bdrop.set_tile(2, 0, Tile("white"))
    bdrop.set_tile(0, 2, Tile("white"))
    bdrop.set_tile(1, 2, Tile("white"))
    bdrop.set_tile(2, 1, Tile("white"))
    bdrop.set_tile(3, 0, Tile("green"))
    bdrop.set_tile(3, 1, Tile("green"))
    bdrop.set_tile(4, 0, Tile("green"))
    print(bdrop)
    bdrop.generate_legal_moves()
    print(bdrop.get_legal_moves())
    print("SCORE:", bdrop.score_backdrop())