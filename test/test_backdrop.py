from backdrop_lib.backdrop import Backdrop, Pixel

if __name__ == "__main__":
    bdrop = Backdrop()
    bdrop.set_tile(0, 0, Pixel("yellow"))
    bdrop.set_tile(0, 1, Pixel("purple"))
    bdrop.set_tile(1, 1, Pixel("green"))
    bdrop.set_tile(1, 0, Pixel("white"))
    bdrop.set_tile(2, 0, Pixel("white"))
    bdrop.set_tile(0, 2, Pixel("white"))
    bdrop.set_tile(1, 2, Pixel("white"))
    bdrop.set_tile(2, 1, Pixel("white"))
    bdrop.set_tile(3, 0, Pixel("green"))
    # bdrop.set_tile(3, 1, Pixel("green"))
    bdrop.generate_legal_moves()
    print(bdrop.get_legal_moves())
    bdrop.set_tile(0, 4, Pixel("green"))
    print(bdrop)
    print("SCORE:", bdrop.calculate_score())
