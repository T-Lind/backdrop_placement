import heapq
import copy
import random
from backdrop import Tile, Backdrop

white_tiles = 8
green_tiles = 3
purple_tiles = 3
yellow_tiles = 3

all_tiles = [Tile("white") for _ in range(white_tiles)] + [Tile("green") for _ in range(green_tiles)] + [Tile("purple")
                                                                                                         for _ in range(
        purple_tiles)] + [Tile("yellow") for _ in range(yellow_tiles)]

random_items = random.sample(all_tiles, white_tiles+green_tiles+purple_tiles+yellow_tiles)
print([random_items[i].identity() for i in range(0, len(random_items))])



class State:
    def __init__(self, backdrop, score):
        self.backdrop = backdrop
        self.score = score

    def __lt__(self, other):
        # Define comparison between states based on their scores
        return self.score < other.score

def estimate_remaining_score_increase(backdrop: Backdrop, remaining_score):
    max_increase = 0
    remaining_tiles = [tile for tile in all_tiles if tile not in backdrop.get_placed_tiles()]

    for tile in remaining_tiles:
        if remaining_score <= 0:
            break
        best_move = None
        best_score_increase = 0

        for move in backdrop.generate_legal_moves():
            temp_backdrop = copy.deepcopy(backdrop)
            temp_backdrop.set_tile(move[0], move[1], tile)
            score_increase = temp_backdrop.calculate_score() - backdrop.calculate_score()

            if score_increase > best_score_increase:
                best_score_increase = score_increase
                best_move = move

        if best_move is not None:
            backdrop.set_tile(best_move[0], best_move[1], tile)
            max_increase += best_score_increase
            remaining_score -= best_score_increase

    return max_increase



def a_star_maximize_score(initial_state, goal_score):
    open_set = []
    closed_set = set()

    # Initialize with the initial state
    heapq.heappush(open_set, (-initial_state.score, initial_state))

    while open_set:
        _, current_state = heapq.heappop(open_set)

        if current_state.score >= goal_score:
            return current_state  # Goal reached

        if current_state in closed_set:
            continue

        closed_set.add(current_state)

        for action in current_state.backdrop.generate_legal_moves():
            # Apply the action to create a new state
            new_backdrop = copy.deepcopy(current_state.backdrop)
            try:
                new_backdrop.set_tile(action[0], action[1], random_items.pop())
            except:
                continue
            new_score = new_backdrop.calculate_score() - current_state.score

            # Create the new state
            new_state = State(new_backdrop, current_state.score + new_score)

            # Use the negative of the score increase as cost
            cost = -new_score

            # Estimate the remaining score increase using a heuristic
            heuristic = estimate_remaining_score_increase(new_backdrop, goal_score - new_state.score)

            # Compute the priority
            priority = new_state.score + cost + heuristic

            # Add the new state to the open set
            heapq.heappush(open_set, (priority, new_state))

    return None  # No solution found

# Example usage
initial_backdrop = Backdrop()  # Replace with actual initialization
goal_score = 180  # Set your desired goal score
initial_state = State(initial_backdrop, 0)

result_state = a_star_maximize_score(initial_state, goal_score)

if result_state:
    print("Goal reached with score:", result_state.score)
    print(result_state.backdrop)
else:
    print("No solution found")
