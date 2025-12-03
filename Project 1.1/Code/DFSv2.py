from typing import List, Tuple, Dict


def dfs_search(dct: Dict) -> List[Tuple[int, int]]:
    rows, cols = dct["rows"], dct["cols"]
    maze = [[0 for _ in range(cols)] for _ in range(rows)]

    for obstacle in dct["obstacles"]:  # Mark obstacles
        row, col = obstacle
        maze[row][col] = 1

    start = tuple(dct["start"])
    goals = set(tuple(goal) for goal in dct["goals"])

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def is_valid_move(row, col):  # Check for out of bounds and obstacle
        return 0 <= row < rows and 0 <= col < cols and maze[row][col] == 0

    def dfs(position):
        row, col = position
        if position in goals:
            return [position]

        maze[row][col] = 2  # Mark the current position as visited

        for dr, dc in moves:
            next_row, next_col = row + dr, col + dc
            if is_valid_move(next_row, next_col):
                path = dfs((next_row, next_col))
                if path:
                    return [position] + path

        # Unmark the current position if no valid path is found (backtrack)
        maze[row][col] = 0
        return None

    path = dfs(start)

    return path if path else []


def visualize_maze(dct: Dict, path: List[Tuple[int, int]] = None):
    rows, cols = dct["rows"], dct["cols"]

    # Create the maze matrix initialized with 0s (free cells)
    maze = [["0" for _ in range(cols)] for _ in range(rows)]

    # Mark obstacles in the maze with 1
    for obstacle in dct["obstacles"]:
        row, col = obstacle
        maze[row][col] = "1"  # 1 represents an obstacle

    # Mark the start position
    start_row, start_col = dct["start"]
    maze[start_row][start_col] = "S"

    # Mark the goal positions
    for goal in dct["goals"]:
        goal_row, goal_col = goal
        maze[goal_row][goal_col] = "G"

    # Mark the path and visited cells if provided
    if path:
        for row, col in path:
            if maze[row][col] == "0":  # Avoid overwriting start or goal
                maze[row][col] = "P"
        for row in range(rows):
            for col in range(cols):
                if maze[row][col] == "0" and maze[row][col] == 2:
                    maze[row][col] = "2"  # Mark visited cells as 2

    # Print the maze
    for row in maze:
        print(" ".join(row))


# import json

# with open(
#     "CS3243-Introduciton to AI/Projects/Project 1.1/Files/upload_testcases/correctness/correctness_public_ab_small_0_99.json",
#     "r",
# ) as f:
#     data = json.load(f)

# # Run the DFS algorithm
# path = dfs_search(data)

# # Visualize the result
# visualize_maze(data, path)
