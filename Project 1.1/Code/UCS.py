from typing import List, Tuple, Dict
import json
import heapq


def ucs_search(dct) -> List[Tuple[int, int]]:
    # YOUR CODE HERE. Do not change the name of the function.
    rows, cols = dct["rows"], dct["cols"]
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    start = tuple(dct["start"])
    goals = set(tuple(goal) for goal in dct["goals"])
    obstacles = set(tuple(obstacle) for obstacle in dct["obstacles"])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Edge Cases
    if start in obstacles:
        return []
    if start in goals:
        return [start]

    for obstacle in obstacles:
        row, col = obstacle
        maze[row][col] = 1  # 1 represents an obstacle

    pq = [(0, start)]
    visited = set()
    parent_map = {}
    cost_map = {start: 0}

    while pq:
        current_cost, position = heapq.heappop(pq)
        row, col = position

        if position in goals:
            path = []
            while position:
                path.append(position)
                position = parent_map.get(position)
            return path[::-1]  # Return reversed path

        if position not in visited:
            visited.add(position)

            for dr, dc in directions:
                next_row, next_col = row + dr, col + dc
                if (
                    0 <= next_row < rows
                    and 0 <= next_col < cols
                    and maze[next_row][next_col] == 0
                ):
                    next_position = (next_row, next_col)
                    new_cost = current_cost + 1
                    if (
                        next_position not in cost_map
                        or new_cost < cost_map[next_position]
                    ):
                        cost_map[next_position] = new_cost
                        heapq.heappush(pq, (new_cost, next_position))
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

path = ucs_search(data)

visualize_maze(data, path)
print(path)
visualize_initial_maze(data)
