from typing import List, Tuple, Dict
import json
from collections import deque


from typing import List, Tuple, Dict
from collections import deque

def bfs_search(dct: Dict) -> List[Tuple[int, int]]:
    rows, cols = dct["rows"], dct["cols"]
    start = tuple(dct["start"])
    goals = {tuple(goal) for goal in dct["goals"]}
    obstacles = {tuple(obstacle) for obstacle in dct["obstacles"]}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    if start in obstacles:
        return []
    if start in goals:
        return [start]

    queue = deque([start])
    visited = {start}
    parent_map = {}

    while queue:
        position = queue.popleft()

        if position in goals:
            path = []
            while position:
                path.append(position)
                position = parent_map.get(position)
            return path[::-1]  # Return reversed path

        row, col = position

        for dr, dc in directions:
            next_position = (row + dr, col + dc)
            next_row, next_col = next_position

            if (
                0 <= next_row < rows  # Check if within row bounds
                and 0 <= next_col < cols  # Check if within column bounds
                and next_position not in obstacles  # Check if not an obstacle
                and next_position not in visited  # Check if not visited
            ):
                visited.add(next_position)
                queue.append(next_position)
                parent_map[next_position] = position

    return []

def visualize_maze(dct: Dict, path: List[Tuple[int, int]] = None):
    rows, cols = dct["rows"], dct["cols"]

    maze = [["0" for _ in range(cols)] for _ in range(rows)]

    for obstacle in dct["obstacles"]:
        row, col = obstacle
        maze[row][col] = "1"

    start_row, start_col = dct["start"]
    maze[start_row][start_col] = "S"

    for goal in dct["goals"]:
        goal_row, goal_col = goal
        maze[goal_row][goal_col] = "G"

    if path:
        for row, col in path:
            if maze[row][col] == "0":
                maze[row][col] = "P"
        for row in range(rows):
            for col in range(cols):
                if maze[row][col] == "0" and maze[row][col] == 2:
                    maze[row][col] = "2"

    for row in maze:
        print(" ".join(row))


def visualize_initial_maze(dct: Dict):
    rows, cols = dct["rows"], dct["cols"]

    maze = [["0" for _ in range(cols)] for _ in range(rows)]

    for obstacle in dct["obstacles"]:
        row, col = obstacle
        maze[row][col] = "1"

    start_row, start_col = dct["start"]
    print(start_row, start_col)
    maze[start_row][start_col] = "S"

    for goal in dct["goals"]:
        goal_row, goal_col = goal
        maze[goal_row][goal_col] = "G"

    for row in maze:
        print(" ".join(row))


with open(
    "CS3243-Introduciton to AI/Projects/Project 1.1/Files/upload_testcases/correctness/correctness_public_dummy_complete_52.json",
    "r",
) as f:
    data = json.load(f)

path = bfs_search(data)

visualize_maze(data, path)
print(path)
visualize_initial_maze(data)
