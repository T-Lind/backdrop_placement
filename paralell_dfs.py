import copy
import random
import multiprocessing
from time import time

from backdrop_lib.backdrop import Pixel, Backdrop

white_pixels = 8
green_pixels = 2
purple_pixels = 2
yellow_pixels = 2


def depth_first_search(current_state: Backdrop, current_sequence, pixels_to_place, best_score, best_score_lock):
    if len(current_sequence) == len(pixels_to_place):
        current_score = current_state.calculate_score()
        if current_score > best_score.value:
            with best_score_lock:
                best_score.value = current_score
                print("New Best Score:", best_score.value)
                print(current_state)
        return

    legal_moves = current_state.generate_legal_moves()
    random.shuffle(legal_moves)
    for move in legal_moves:
        new_state = copy.deepcopy(current_state)
        new_state.set_pixel(move[0], move[1], pixels_to_place[len(current_sequence)])
        new_sequence = current_sequence + [move]
        depth_first_search(new_state, new_sequence, pixels_to_place, best_score, best_score_lock)


def parallel_search(initial_backdrop, random_items, process_count):
    manager = multiprocessing.Manager()
    best_score = manager.Value('i', float('-inf'))
    best_score_lock = manager.Lock()

    pool = multiprocessing.Pool(process_count)
    for _ in range(process_count):
        pool.apply_async(depth_first_search, (initial_backdrop, [], random_items, best_score, best_score_lock))

    pool.close()
    pool.join()

    return best_score.value


if __name__ == "__main__":
    all_pixels = [Pixel("white") for _ in range(white_pixels)] + [Pixel("green") for _ in range(green_pixels)] + [
        Pixel("purple")
        for _ in range(
            purple_pixels)] + [Pixel("yellow") for _ in range(yellow_pixels)]

    random.shuffle(all_pixels)
    random_items = all_pixels
    print("Starting...")
    print([random_items[i].identity() for i in range(0, len(random_items))])

    initial_backdrop = Backdrop()
    process_count = 3  # Adjust this to the desired number of processes

    start_time = time()
    best_score = parallel_search(initial_backdrop, random_items, process_count)
    end_time = time()

    print("BEST RESULT".center(80, "-"))
    print("Best Score:", best_score)
    print("Time taken:", end_time - start_time, "s")
