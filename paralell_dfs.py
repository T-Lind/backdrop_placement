import copy
import random
from backdrop_lib.backdrop import Tile, Backdrop
from multiprocessing import Pool, Manager
white_tiles = 15
green_tiles = 5
purple_tiles = 5
yellow_tiles = 5

all_tiles = [Tile("white") for _ in range(white_tiles)] + [Tile("green") for _ in range(green_tiles)] + [Tile("purple")
                                                                                                         for _ in range(
        purple_tiles)] + [Tile("yellow") for _ in range(yellow_tiles)]

random_items = random.sample(all_tiles, white_tiles + green_tiles + purple_tiles + yellow_tiles)
print([random_items[i].identity() for i in range(0, len(random_items))])

def parallel_search(params):
    current_state, current_sequence, tiles_to_place, best_sequence, best_score = params
    if len(current_sequence) == len(tiles_to_place):
        # Reached the end of the sequence, evaluate the score
        current_score = current_state.calculate_score()
        if current_score > best_score[0]:
            best_score[0] = current_score
            best_sequence[0] = current_sequence[:]
            print("New Best Score for the following:", best_score[0])
            print(current_state)
    else:
        # Generate all possible moves for the next tile
        legal_moves = current_state.generate_legal_moves()
        for move in legal_moves:
            new_state = copy.deepcopy(current_state)
            new_state.set_tile(move[0], move[1], tiles_to_place[len(current_sequence)])
            new_sequence = current_sequence + [move]
            parallel_search((new_state, new_sequence, tiles_to_place, best_sequence, best_score))


if __name__ == "__main__":
    # Create your initial backdrop object
    initial_backdrop = Backdrop()  # Replace with actual initialization

    # Perform depth-first search with parallel processing
    best_sequence = Manager().list([[]])
    best_score = Manager().list([float('-inf')])

    # Split the work into multiple processes
    num_processes = 8  # Adjust this as needed
    params_list = [(initial_backdrop, [], random_items, best_sequence, best_score) for _ in range(num_processes)]

    with Pool(num_processes) as pool:
        pool.map(parallel_search, params_list)

    # Apply the best sequence of moves
    for move in best_sequence[0]:
        initial_backdrop.set_tile(move[0], move[1], random_items[initial_backdrop.get_num_placed_tiles()])

    print(initial_backdrop)
    print("Best Sequence:", best_sequence[0])
    print("Best Score:", initial_backdrop.calculate_score())
