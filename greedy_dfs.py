import copy
import random

from backdrop_lib.backdrop import Pixel, Backdrop
from time import time

white_pixels = 5
green_pixels = 1
purple_pixels = 1
yellow_pixels = 1

all_pixels = [Pixel("white") for _ in range(white_pixels)] + [Pixel("green") for _ in range(green_pixels)] + [Pixel("purple")
                                                                                                           for _ in range(
        purple_pixels)] + [Pixel("yellow") for _ in range(yellow_pixels)]

random_items = random.sample(all_pixels, white_pixels + green_pixels + purple_pixels + yellow_pixels)
print([random_items[i].identity() for i in range(0, len(random_items))])


def depth_first_search(current_state: Backdrop, current_sequence, pixels_to_place, best_score):
    if len(current_sequence) == len(pixels_to_place):
        # Reached the end of the sequence, evaluate the score
        current_score = current_state.calculate_score()
        if current_score > best_score[0]:
            best_score[0] = current_score
            best_sequence[0] = current_sequence
            print("New Best Score for the following:", best_score[0])
            print(current_state)
    else:
        # Generate all possible moves for the next pixel
        legal_moves = current_state.generate_legal_moves()
        scored_moves = []
        for move in legal_moves:
            new_state = copy.deepcopy(current_state)
            new_state.set_pixel(move[0], move[1], pixels_to_place[len(current_sequence)])
            # Get the score:
            new_score = new_state.calculate_score()
            scored_moves.append((move, new_score))
        # Sort the moves by score
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        for move, score in scored_moves:
            new_state = copy.deepcopy(current_state)
            new_state.set_pixel(move[0], move[1], pixels_to_place[len(current_sequence)])
            new_sequence = current_sequence + [move]
            depth_first_search(new_state, new_sequence, pixels_to_place, best_score)


# Create your initial backdrop object
initial_backdrop = Backdrop()  # Replace with actual initialization

# Perform depth-first search
best_sequence = [[]]
best_score = [float('-inf')]

start_time = time()
depth_first_search(initial_backdrop, [], random_items, best_score)
end_time = time()

print("BEST RESULT".center(80, "-"))
# Apply the best sequence of moves
for move in best_sequence[0]:
    initial_backdrop.set_pixel(move[0], move[1], random_items[initial_backdrop.get_num_placed_pixels()])
print(initial_backdrop)
print("Best Sequence:", best_sequence[0])
print("Best Score:", initial_backdrop.calculate_score())

print("Time taken:", end_time - start_time, "s")
