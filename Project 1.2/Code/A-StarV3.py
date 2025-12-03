import heapq
from typing import List, Dict, Tuple
from enum import Enum
import copy


# Define Actions
class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    FLASH = 4
    NUKE = 5


# Directions for movement
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP  # DOWN  # LEFT  # RIGHT


# A* Search function
def search(dct: Dict) -> List[int]:
    # Extract input data
    cols, rows = dct["cols"], dct["rows"]
    start = tuple(dct["start"])  # Starting position
    goals = set(tuple(goal) for goal in dct["goals"])  # Goal positions (runes)
    obstacles = set(tuple(obstacle) for obstacle in dct["obstacles"])  # Obstacles
    creeps = {
        tuple([x, y]): num_creeps for (x, y, num_creeps) in dct["creeps"]
    }  # Creeps info
    num_flash_left = dct["num_flash_left"]  # Max number of FLASH uses
    num_nuke_left = dct["num_nuke_left"]  # Max number of NUKE uses

    # Priority queue for A* search (min-heap)
    pq = []
    # Initial state: (total cost so far, heuristic cost, position, remaining FLASH, remaining NUKE, path, creeps)
    heapq.heappush(
        pq,
        (0, heuristic(start, goals), start, num_flash_left, num_nuke_left, [], creeps),
    )

    # Dictionary to store the best cost for each state (position, flash, nuke)
    best_cost = {}

    while pq:
        total_cost, _, current_pos, flash_left, nuke_left, path, creeps_state = (
            heapq.heappop(pq)
        )

        # Check if we've reached a goal
        if current_pos in goals:
            return path

        # Avoid revisiting worse or duplicate states
        state_key = (current_pos, flash_left, nuke_left)
        if state_key in best_cost and best_cost[state_key] <= total_cost:
            continue
        best_cost[state_key] = total_cost

        # Generate next possible states (regular moves)
        for idx, (dx, dy) in enumerate(DIRECTIONS):
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if valid_move(new_pos, rows, cols, obstacles):
                # Calculate movement cost in one pass
                move_cost = total_cost + 4 + creeps_state.get(new_pos, 0)
                heapq.heappush(
                    pq,
                    (
                        move_cost,
                        move_cost + heuristic(new_pos, goals),
                        new_pos,
                        flash_left,
                        nuke_left,
                        path + [Action(idx).value],
                        creeps_state,
                    ),
                )

        # FLASH skill
        if flash_left > 0:
            for idx, (dx, dy) in enumerate(DIRECTIONS):
                new_pos, flash_cost = single_pass_flash(
                    current_pos, dx, dy, rows, cols, obstacles, creeps_state
                )
                cost = total_cost + 10 + flash_cost  # FLASH cost
                heapq.heappush(
                    pq,
                    (
                        cost,
                        cost + heuristic(new_pos, goals),
                        new_pos,
                        flash_left - 1,
                        nuke_left,
                        path + [Action.FLASH.value, Action(idx).value],
                        creeps_state,
                    ),
                )

        # NUKE skill
        if nuke_left > 0:
            new_creeps_state = apply_nuke(
                current_pos, creeps_state
            )  # Apply NUKE on a copy of the creeps
            cost = total_cost + 50  # NUKE cost
            heapq.heappush(
                pq,
                (
                    cost,
                    cost + heuristic(current_pos, goals),
                    current_pos,
                    flash_left,
                    nuke_left - 1,
                    path + [Action.NUKE.value],
                    new_creeps_state,
                ),
            )

    return []  # Return empty list if no path is found


# Optimized Heuristic function (Manhattan distance)
def heuristic(pos: Tuple[int, int], goals: set) -> int:
    return min(abs(pos[0] - g[0]) + abs(pos[1] - g[1]) for g in goals)


# Validate move within the dungeon bounds and not into obstacles
def valid_move(pos: Tuple[int, int], rows: int, cols: int, obstacles: set) -> bool:
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols and pos not in obstacles


# Single-pass Flash move function
def single_pass_flash(
    start: Tuple[int, int],
    dx: int,
    dy: int,
    rows: int,
    cols: int,
    obstacles: set,
    creeps: dict,
):
    pos = start
    total_cost = 0
    while True:
        new_pos = (pos[0] + dx, pos[1] + dy)
        if not valid_move(new_pos, rows, cols, obstacles):
            break
        pos = new_pos
        total_cost += 2 + creeps.get(pos, 0)  # FLASH reduces movement cost to 2 MP
    return pos, total_cost


# Apply NUKE in one pass (copy creeps state)
def apply_nuke(pos: Tuple[int, int], creeps: dict) -> dict:
    new_creeps = copy.deepcopy(creeps)  # Make a copy to avoid modifying global state
    for (x, y), num in creeps.items():
        if abs(x - pos[0]) + abs(y - pos[1]) <= 10:
            new_creeps[(x, y)] = 0  # Remove all creeps within Manhattan distance 10
    return new_creeps


# 27/30 2/3
