import copy
import random

from backdrop import Tile, Backdrop

white_tiles = 15
green_tiles = 5
purple_tiles = 5
yellow_tiles = 5

all_tiles = [Tile("white") for _ in range(white_tiles)] + [Tile("green") for _ in range(green_tiles)] + [Tile("purple")
                                                                                                         for _ in range(
        purple_tiles)] + [Tile("yellow") for _ in range(yellow_tiles)]

random_items = random.sample(all_tiles, 30)
print([random_items[i].identity() for i in range(0, len(random_items))])


def make_best_choice(tile: Tile, backdrop: Backdrop):
    legal_moves = backdrop.generate_legal_moves()
    print(legal_moves)
    scores = []
    for move in legal_moves:
        local_backdrop = copy.deepcopy(backdrop)
        local_backdrop.set_tile(move[0], move[1], tile)
        score = local_backdrop.calculate_score()
        scores.append(score)
        print("The following backdrop's score is:", score)
        print(local_backdrop)

    best_move = legal_moves[scores.index(max(scores))]
    backdrop.set_tile(best_move[0], best_move[1], tile)
    print(scores)


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
# bdrop.set_tile(3, 1, Tile("green"))
make_best_choice(Tile("green"), bdrop)
print(bdrop)
