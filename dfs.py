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

random_items = random.sample(all_tiles, white_tiles + green_tiles + purple_tiles + yellow_tiles)
print([random_items[i].identity() for i in range(0, len(random_items))])

def depth_first_search(current_state: Backdrop, current_sequence, tiles_to_place, best_score):
    if len(current_sequence) == len(tiles_to_place):
        # Reached the end of the sequence, evaluate the score
        current_score = current_state.calculate_score()
        if current_score > best_score[0]:
            best_score[0] = current_score
            best_sequence[0] = current_sequence
            print("New Best Score for the following:", best_score[0])
            print(current_state)
    else:
        # Generate all possible moves for the next tile
        legal_moves = current_state.generate_legal_moves()
        for move in legal_moves:
            new_state = copy.deepcopy(current_state)
            new_state.set_tile(move[0], move[1], tiles_to_place[len(current_sequence)])
            new_sequence = current_sequence + [move]
            depth_first_search(new_state, new_sequence, tiles_to_place, best_score)

# Create your initial backdrop object
initial_backdrop = Backdrop()  # Replace with actual initialization

# Perform depth-first search
best_sequence = [[]]
best_score = [float('-inf')]
depth_first_search(initial_backdrop, [], random_items, best_score)

# Apply the best sequence of moves
for move in best_sequence[0]:
    initial_backdrop.set_tile(move[0], move[1], random_items[initial_backdrop.get_num_placed_tiles()])
print(initial_backdrop)
print("Best Sequence:", best_sequence[0])
print("Best Score:", initial_backdrop.calculate_score())
