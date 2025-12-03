from queue import PriorityQueue
from enum import Enum
from typing import List, Dict, Tuple


# Define action enum for UP, DOWN, LEFT, RIGHT, FLASH, NUKE
class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    FLASH = 4
    NUKE = 5


# Heuristic function: Manhattan distance between two points
def heuristic(
    curr_pos: Tuple[int, int], goal_pos: Tuple[int, int], weight: float = 1.0
) -> int:
    return weight * (abs(curr_pos[0] - goal_pos[0]) + abs(curr_pos[1] - goal_pos[1]))


# Calculate the total MP cost of moving to a cell, considering creeps
def calculate_cost(
    position: Tuple[int, int], creeps: Dict[Tuple[int, int], int], action_cost: int = 4
) -> int:
    return action_cost + creeps.get(position, 0)


# Check if FLASH is beneficial by comparing the costs
def should_use_flash(g: int, cells_traversed: int, creeps_encountered: int) -> bool:
    flash_cost = g + 10 + (2 * cells_traversed) + creeps_encountered
    normal_cost = g + (4 * cells_traversed) + creeps_encountered
    return flash_cost < normal_cost


# Handle FLASH movement
def handle_flash(
    pq: PriorityQueue,
    current_pos: Tuple[int, int],
    directions: Dict[Action, Tuple[int, int]],
    g: int,
    flash_left: int,
    nuke_left: int,
    actions: List[int],
    visited: Dict[Tuple[int, int, int], int],
    creeps: Dict[Tuple[int, int], int],
    rows: int,
    cols: int,
    goals: List[Tuple[int, int]],
    obstacles: set,
):
    for action, (dx, dy) in directions.items():
        new_pos = current_pos
        cells_traversed = 0
        creeps_encountered = 0

        # Move in the direction until hitting an obstacle or boundary
        while (
            0 <= new_pos[0] + dx < rows
            and 0 <= new_pos[1] + dy < cols
            and (new_pos[0] + dx, new_pos[1] + dy) not in obstacles
        ):
            new_pos = (new_pos[0] + dx, new_pos[1] + dy)
            cells_traversed += 1
            creeps_encountered += creeps.get(new_pos, 0)

        # Only use FLASH if it's cheaper
        if should_use_flash(g, cells_traversed, creeps_encountered):
            new_g = g + 10 + (2 * cells_traversed) + creeps_encountered
            if (new_pos, flash_left - 1, nuke_left) not in visited or new_g < visited[
                (new_pos, flash_left - 1, nuke_left)
            ]:
                visited[(new_pos, flash_left - 1, nuke_left)] = new_g
                h = min(heuristic(new_pos, goal) for goal in goals)
                pq.put(
                    (
                        new_g + h,
                        new_g,
                        new_pos,
                        actions + [Action.FLASH.value, action.value],
                        flash_left - 1,
                        nuke_left,
                    )
                )


# Check if using NUKE is beneficial
def should_use_nuke(total_creeps_in_radius: int) -> bool:
    return total_creeps_in_radius * 4 > 50


# Handle NUKE action
def handle_nuke(
    pq: PriorityQueue,
    current_pos: Tuple[int, int],
    g: int,
    flash_left: int,
    nuke_left: int,
    actions: List[int],
    visited: Dict[Tuple[int, int, int], int],
    creeps: Dict[Tuple[int, int], int],
    rows: int,
    cols: int,
    goals: List[Tuple[int, int]],
):
    # Check total creeps in a 10-Manhattan radius
    total_creeps_in_radius = sum(
        creeps.get((current_pos[0] + i, current_pos[1] + j), 0)
        for i in range(-10, 11)
        for j in range(-10, 11)
        if abs(i) + abs(j) <= 10
    )

    # If beneficial, apply NUKE
    if should_use_nuke(total_creeps_in_radius):
        creeps_after_nuke = creeps.copy()
        for i in range(-10, 11):
            for j in range(-10, 11):
                if abs(i) + abs(j) <= 10:
                    nuke_pos = (current_pos[0] + i, current_pos[1] + j)
                    if 0 <= nuke_pos[0] < rows and 0 <= nuke_pos[1] < cols:
                        creeps_after_nuke[nuke_pos] = 0

        pq.put(
            (g + 50, g + 50, current_pos, actions + [Action.NUKE.value], flash_left, 0)
        )
        return creeps_after_nuke
    return creeps


# Main search function
def search(dct) -> List[int]:
    rows, cols = dct["rows"], dct["cols"]
    obstacles = set(tuple(o) for o in dct["obstacles"])
    creeps = {tuple(creep[:2]): creep[2] for creep in dct["creeps"]}
    start = tuple(dct["start"])
    goals = [tuple(goal) for goal in dct["goals"]]
    num_flash_left = dct["num_flash_left"]
    num_nuke_left = dct["num_nuke_left"]

    # Directions mapping for UP, DOWN, LEFT, RIGHT
    directions = {
        Action.UP: (-1, 0),
        Action.DOWN: (1, 0),
        Action.LEFT: (0, -1),
        Action.RIGHT: (0, 1),
    }

    # Priority Queue for A* (f, g, position, action_sequence, flash_left, nuke_left)
    pq = PriorityQueue()
    pq.put((0, 0, start, [], num_flash_left, num_nuke_left))
    visited = {(start, num_flash_left, num_nuke_left): 0}

    if start in obstacles:
        return []

    while not pq.empty():
        f, g, current_pos, actions, flash_left, nuke_left = pq.get()

        # If we reach a goal, return the action sequence
        if current_pos in goals:
            return actions

        # Explore the neighboring positions for basic movements
        for action, (dx, dy) in directions.items():
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)

            if (
                0 <= new_pos[0] < rows
                and 0 <= new_pos[1] < cols
                and new_pos not in obstacles
            ):
                new_g = g + calculate_cost(new_pos, creeps)

                if (new_pos, flash_left, nuke_left) not in visited or new_g < visited[
                    (new_pos, flash_left, nuke_left)
                ]:
                    visited[(new_pos, flash_left, nuke_left)] = new_g
                    h = min(heuristic(new_pos, goal) for goal in goals)
                    pq.put(
                        (
                            new_g + h,
                            new_g,
                            new_pos,
                            actions + [action.value],
                            flash_left,
                            nuke_left,
                        )
                    )

        # Handle FLASH movement
        if flash_left > 0:
            handle_flash(
                pq,
                current_pos,
                directions,
                g,
                flash_left,
                nuke_left,
                actions,
                visited,
                creeps,
                rows,
                cols,
                goals,
                obstacles,
            )

        # Handle NUKE action if available
        if nuke_left > 0:
            creeps = handle_nuke(
                pq,
                current_pos,
                g,
                flash_left,
                nuke_left,
                actions,
                visited,
                creeps,
                rows,
                cols,
                goals,
            )

    return []
