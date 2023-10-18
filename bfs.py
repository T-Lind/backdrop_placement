import copy
import random
from backdrop_lib.backdrop import Pixel, Backdrop
from time import time

white_pixels = 15
green_pixels = 5
purple_pixels = 5
yellow_pixels = 5

all_pixels = [Pixel("white") for _ in range(white_pixels)] + [Pixel("green") for _ in range(green_pixels)] + [Pixel("purple")
                                                                                                           for _ in range(
        purple_pixels)] + [Pixel("yellow") for _ in range(yellow_pixels)]

random_items = random.sample(all_pixels, white_pixels + green_pixels + purple_pixels + yellow_pixels)
print([random_items[i].identity() for i in range(0, len(random_items))])


def breadth_first_search(initial_state, pixels_to_place):
    queue = [(initial_state, [])]
    best_score = float('-inf')
    best_sequence = []

    while queue:
        current_state, current_sequence = queue.pop(0)
        if len(current_sequence) == len(pixels_to_place):
            # Reached the end of the sequence, evaluate the score
            current_score = current_state.calculate_score()
            if current_score > best_score:
                best_score = current_score
                best_sequence = current_sequence
                print("New Best Score for the following:", best_score)
                print(current_state)
        else:
            # Generate all possible moves for the next pixel
            legal_moves = current_state.generate_legal_moves()
            for move in legal_moves:
                new_state = copy.deepcopy(current_state)
                new_state.set_pixel(move[0], move[1], pixels_to_place[len(current_sequence)])
                new_sequence = current_sequence + [move]
                queue.append((new_state, new_sequence))

    return best_sequence


# Create your initial backdrop object
initial_backdrop = Backdrop()  # Replace with actual initialization

# Perform breadth-first search
before_time = time()
best_sequence = breadth_first_search(initial_backdrop, random_items)
end_time = time()

# Apply the best sequence of moves
for move in best_sequence:
    initial_backdrop.set_pixel(move[0], move[1], random_items[initial_backdrop.get_num_placed_pixels()])
print(initial_backdrop)
print("Best Sequence:", best_sequence)
print("Best Score:", initial_backdrop.calculate_score())

print("Time taken:", end_time - before_time, "s")
