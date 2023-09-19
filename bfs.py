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


def breadth_first_search(initial_state, tiles_to_place):
    queue = [(initial_state, [])]
    best_score = float('-inf')
    best_sequence = []

    while queue:
        current_state, current_sequence = queue.pop(0)
        if len(current_sequence) == len(tiles_to_place):
            # Reached the end of the sequence, evaluate the score
            current_score = current_state.calculate_score()
            if current_score > best_score:
                best_score = current_score
                best_sequence = current_sequence
                print("New Best Score for the following:", best_score)
                print(current_state)
        else:
            # Generate all possible moves for the next tile
            legal_moves = current_state.generate_legal_moves()
            for move in legal_moves:
                new_state = copy.deepcopy(current_state)
                new_state.set_tile(move[0], move[1], tiles_to_place[len(current_sequence)])
                new_sequence = current_sequence + [move]
                queue.append((new_state, new_sequence))

    return best_sequence


# Create your initial backdrop object
initial_backdrop = Backdrop()  # Replace with actual initialization

# Perform breadth-first search
best_sequence = breadth_first_search(initial_backdrop, random_items)

# Apply the best sequence of moves
for move in best_sequence:
    initial_backdrop.set_tile(move[0], move[1], random_items[initial_backdrop.get_num_placed_tiles()])
print(initial_backdrop)
print("Best Sequence:", best_sequence)
print("Best Score:", initial_backdrop.calculate_score())
