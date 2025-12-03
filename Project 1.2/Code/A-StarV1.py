from queue import PriorityQueue
from enum import Enum
from typing import List, Dict, Tuple

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    FLASH = 4
    NUKE = 5

def heuristic(curr_pos: Tuple[int, int], goal_pos: Tuple[int, int], weight: float = 1.0) -> int:
    return weight * (abs(curr_pos[0] - goal_pos[0]) + abs(curr_pos[1] - goal_pos[1]))

def calculate_cost(position: Tuple[int, int], creeps: Dict[Tuple[int, int], int], action_cost: int = 4) -> int:
    return action_cost + creeps.get(position, 0)

def find_best_path(dct) -> Tuple[List[int], List[Tuple[int, int]]]:
    rows, cols = dct["rows"], dct["cols"]
    obstacles = set(tuple(o) for o in dct["obstacles"])
    creeps = {tuple(creep[:2]): creep[2] for creep in dct["creeps"]}
    start = tuple(dct["start"])
    goals = [tuple(goal) for goal in dct["goals"]]

    directions = {
        Action.UP: (-1, 0),
        Action.DOWN: (1, 0),
        Action.LEFT: (0, -1),
        Action.RIGHT: (0, 1),
    }

    pq = PriorityQueue()
    pq.put((0, 0, start, [], [start]))
    visited = {start: 0}

    if start in obstacles:
        return [], []

    while not pq.empty():
        f, g, current_pos, actions, path = pq.get()

        if current_pos in goals:
            return actions, path

        for action, (dx, dy) in directions.items():
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)

            if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and new_pos not in obstacles:
                new_g = g + calculate_cost(new_pos, creeps)

                if new_pos not in visited or new_g < visited[new_pos]:
                    visited[new_pos] = new_g
                    h = min(heuristic(new_pos, goal) for goal in goals)
                    pq.put((new_g + h, new_g, new_pos, actions + [action.value], path + [new_pos]))

    return [], []

def optimize_path_with_flash_and_nuke(path: List[Tuple[int, int]], dct) -> List[int]:
    optimized_actions = []
    num_flash_left = dct["num_flash_left"]
    num_nuke_left = dct["num_nuke_left"]
    creeps = {tuple(creep[:2]): creep[2] for creep in dct["creeps"]}
    obstacles = set(tuple(o) for o in dct["obstacles"])

    directions = {
        (-1, 0): Action.UP,
        (1, 0): Action.DOWN,
        (0, -1): Action.LEFT,
        (0, 1): Action.RIGHT,
    }

    i = 0
    while i < len(path) - 1:
        current_pos = path[i]
        next_pos = path[i + 1]
        move = (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])

        action = directions[move]
        optimized_actions.append(action.value)

        if num_flash_left > 0:
            straight_line_steps = 0
            obstacle_in_path = False
            for j in range(i + 1, len(path) - 1):
                next_step = path[j + 1]
                if (next_step[0] - path[j][0], next_step[1] - path[j][1]) == move:
                    if next_step in obstacles:
                        obstacle_in_path = True
                        break
                    straight_line_steps += 1
                else:
                    break

            if straight_line_steps >= 2 and not obstacle_in_path:
                optimized_actions[-1] = Action.FLASH.value
                num_flash_left -= 1
                i += straight_line_steps
            else:
                i += 1
        else:
            i += 1

        if num_nuke_left > 0:
            creeps_in_radius = sum(creeps.get(path[j], 0) for j in range(i, min(i + 10, len(path))))
            if creeps_in_radius > 50:
                optimized_actions.append(Action.NUKE.value)
                num_nuke_left -= 1

    return optimized_actions

def search(dct) -> List[int]:
    actions, path = find_best_path(dct)

    if not path:
        return []

    optimized_actions = optimize_path_with_flash_and_nuke(path, dct)

    return optimized_actions
