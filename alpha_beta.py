import copy
import random
from backdrop import Tile, Backdrop

def minimax_alpha_beta(initial_state, tiles_to_place, depth, alpha, beta, maximizing_player):
    if depth == 0 or len(tiles_to_place) == 0:
        return initial_state.calculate_score(), []

    if maximizing_player:
        max_score = float('-inf')
        best_sequence = []

        legal_moves = initial_state.generate_legal_moves()
        for move in legal_moves:
            new_state = copy.deepcopy(initial_state)
            new_state.set_tile(move[0], move[1], tiles_to_place[0])
            new_tiles_to_place = tiles_to_place[1:]
            score, sequence = minimax_alpha_beta(new_state, new_tiles_to_place, depth - 1, alpha, beta, False)

            if score > max_score:
                max_score = score
                best_sequence = [move] + sequence

            alpha = max(alpha, max_score)
            if beta <= alpha:
                break  # Prune the remaining branches

        return max_score, best_sequence
    else:
        min_score = float('inf')
        best_sequence = []

        legal_moves = initial_state.generate_legal_moves()
        for move in legal_moves:
            new_state = copy.deepcopy(initial_state)
            new_state.set_tile(move[0], move[1], tiles_to_place[0])
            new_tiles_to_place = tiles_to_place[1:]
            score, sequence = minimax_alpha_beta(new_state, new_tiles_to_place, depth - 1, alpha, beta, True)

            if score < min_score:
                min_score = score
                best_sequence = [move] + sequence

            beta = min(beta, min_score)
            if beta <= alpha:
                break  # Prune the remaining branches

        return min_score, best_sequence

def breadth_first_search_alpha_beta(initial_state, tiles_to_place, depth):
    _, best_sequence = minimax_alpha_beta(initial_state, tiles_to_place, depth, float('-inf'), float('inf'), True)
    return best_sequence



white_tiles = 5
green_tiles = 2
purple_tiles = 2
yellow_tiles = 2

all_tiles = [Tile("white") for _ in range(white_tiles)] + [Tile("green") for _ in range(green_tiles)] + [Tile("purple")
                                                                                                         for _ in range(
        purple_tiles)] + [Tile("yellow") for _ in range(yellow_tiles)]

random_items = random.sample(all_tiles, white_tiles + green_tiles + purple_tiles + yellow_tiles)
print([random_items[i].identity() for i in range(0, len(random_items))])

initial_backdrop = Backdrop()

# Set the depth to control the search depth
depth = 100  # You can adjust this value as needed

# Perform breadth-first search with alpha-beta pruning
best_sequence = breadth_first_search_alpha_beta(initial_backdrop, random_items, depth)

# Apply the best sequence of moves
for move in best_sequence:
    initial_backdrop.set_tile(move[0], move[1], random_items[initial_backdrop.get_num_placed_tiles()])

# Print the result
print(initial_backdrop)
print("Best Sequence:", best_sequence)
print("Best Score:", initial_backdrop.calculate_score())
