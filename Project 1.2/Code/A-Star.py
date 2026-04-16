import heapq
from typing import List, Dict, Tuple
from enum import Enum

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    FLASH = 4
    NUKE = 5

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def enhanced_heuristic(pos: Tuple[int, int], goals: set, creeps: Dict[Tuple[int, int], int], obstacles: set, flash_left: int) -> int:
    manhattan_dist = min(abs(pos[0] - g[0]) + abs(pos[1] - g[1]) for g in goals)
    creep_penalty = 0
    for goal in goals:
        x_diff = goal[0] - pos[0]
        y_diff = goal[1] - pos[1]
        if x_diff == 0 or y_diff == 0:
            for i in range(min(pos[0], goal[0]), max(pos[0], goal[0]) + 1):
                for j in range(min(pos[1], goal[1]), max(pos[1], goal[1]) + 1):
                    if (i, j) in creeps:
                        creep_penalty += creeps[(i, j)]
    flash_savings = 0
    if flash_left > 0:
        flash_savings = 8
    return manhattan_dist + creep_penalty - flash_savings

def modified_search(dct: Dict) -> List[int]:
    cols, rows = dct["cols"], dct["rows"]
    start = tuple(dct["start"])
    goals = set(tuple(goal) for goal in dct["goals"])
    obstacles = set(tuple(obstacle) for obstacle in dct["obstacles"])
    creeps = {tuple([x, y]): num_creeps for (x, y, num_creeps) in dct["creeps"]}
    num_flash_left = dct["num_flash_left"]
    num_nuke_left = dct["num_nuke_left"]
    
    pq = []
    heapq.heappush(
        pq,
        (0, enhanced_heuristic(start, goals, creeps, obstacles, num_flash_left), start, num_flash_left, num_nuke_left, [], creeps),
    )
    
    best_cost = {}
    
    while pq:
        total_cost, _, current_pos, flash_left, nuke_left, path, creeps_state = heapq.heappop(pq)
        
        if current_pos in goals:
            return path
        
        state_key = (current_pos, flash_left, nuke_left)
        if state_key in best_cost and best_cost[state_key] <= total_cost:
            continue
        best_cost[state_key] = total_cost
        
        for idx, (dx, dy) in enumerate(DIRECTIONS):
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if valid_move(new_pos, rows, cols, obstacles):
                move_cost = total_cost + 4 + creeps_state.get(new_pos, 0)
                heapq.heappush(
                    pq,
                    (
                        move_cost,
                        move_cost + enhanced_heuristic(new_pos, goals, creeps_state, obstacles, flash_left),
                        new_pos,
                        flash_left,
                        nuke_left,
                        path + [Action(idx).value],
                        creeps_state,
                    ),
                )
        
        if flash_left > 0:
            for idx, (dx, dy) in enumerate(DIRECTIONS):
                new_pos, flash_cost = single_pass_flash(
                    current_pos, dx, dy, rows, cols, obstacles, creeps_state
                )
                if flash_cost + 10 < (4 * abs(current_pos[0] - new_pos[0]) + abs(current_pos[1] - new_pos[1])):
                    cost = total_cost + 10 + flash_cost
                    heapq.heappush(
                        pq,
                        (
                            cost,
                            cost + enhanced_heuristic(new_pos, goals, creeps_state, obstacles, flash_left - 1),
                            new_pos,
                            flash_left - 1,
                            nuke_left,
                            path + [Action.FLASH.value, Action(idx).value],
                            creeps_state,
                        ),
                    )
        
        if nuke_left > 0:
            creeps_in_radius = sum(
                creeps_state.get((current_pos[0] + dx, current_pos[1] + dy), 0)
                for dx in range(-10, 11)
                for dy in range(-10, 11)
                if abs(dx) + abs(dy) <= 10 and valid_move((current_pos[0] + dx, current_pos[1] + dy), rows, cols, obstacles)
            )
            if creeps_in_radius > 50:
                new_creeps_state = apply_nuke(current_pos, creeps_state)
                cost = total_cost + 50
                heapq.heappush(
                    pq,
                    (
                        cost,
                        cost + enhanced_heuristic(current_pos, goals, new_creeps_state, obstacles, flash_left),
                        current_pos,
                        flash_left,
                        nuke_left - 1,
                        path + [Action.NUKE.value],
                        new_creeps_state,
                    ),
                )
    
    return []

def valid_move(pos: Tuple[int, int], rows: int, cols: int, obstacles: set) -> bool:
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols and pos not in obstacles

def single_pass_flash(start: Tuple[int, int], dx: int, dy: int, rows: int, cols: int, obstacles: set, creeps_state: Dict[Tuple[int, int], int]):
    pass

def apply_nuke(current_pos: Tuple[int, int], creeps_state: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], int]:
    pass
