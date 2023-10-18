import copy
import random

from backdrop_lib.backdrop import Pixel, Backdrop

white_pixels = 15
green_pixels = 5
purple_pixels = 5
yellow_pixels = 5

all_pixels = [Pixel("white") for _ in range(white_pixels)] + [Pixel("green") for _ in range(green_pixels)] + [Pixel("purple")
                                                                                                           for _ in range(
        purple_pixels)] + [Pixel("yellow") for _ in range(yellow_pixels)]

random_items = random.sample(all_pixels, 30)
print([random_items[i].identity() for i in range(0, len(random_items))])


def make_best_choice(pixel: Pixel, backdrop: Backdrop):
    legal_moves = backdrop.generate_legal_moves()
    print(legal_moves)
    scores = []
    for move in legal_moves:
        local_backdrop = copy.deepcopy(backdrop)
        local_backdrop.set_pixel(move[0], move[1], pixel)
        score = local_backdrop.calculate_score()
        scores.append(score)
        print("The following backdrop's score is:", score)
        print(local_backdrop)

    best_move = legal_moves[scores.index(max(scores))]
    backdrop.set_pixel(best_move[0], best_move[1], pixel)
    print(scores)


bdrop = Backdrop()
bdrop.set_pixel(0, 0, Pixel("yellow"))
bdrop.set_pixel(0, 1, Pixel("purple"))
bdrop.set_pixel(1, 1, Pixel("green"))
bdrop.set_pixel(1, 0, Pixel("white"))
bdrop.set_pixel(2, 0, Pixel("white"))
bdrop.set_pixel(0, 2, Pixel("white"))
bdrop.set_pixel(1, 2, Pixel("white"))
bdrop.set_pixel(2, 1, Pixel("white"))
bdrop.set_pixel(3, 0, Pixel("green"))
# bdrop.set_pixel(3, 1, Pixel("green"))
make_best_choice(Pixel("green"), bdrop)
print(bdrop)
