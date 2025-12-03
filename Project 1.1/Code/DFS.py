from typing import List, Tuple, Dict, Set


def dfs_search(dct: Dict) -> List[Tuple[int, int]]:
    rows, cols = dct["rows"], dct["cols"]
    start_node = tuple(dct["start"])
    goals = {tuple(goal) for goal in dct["goals"]}
    obstacles = {tuple(obstacle) for obstacle in dct["obstacles"]}

    # Initialize the frontier as a stack
    frontier = [(start_node, [start_node])]

    if start_node in goals:
        return [start_node]

    while frontier:
        current_node, path = frontier.pop()

        if current_node in goals:
            return path
        obstacles.add(current_node)

        crow = current_node[0]
        ccol = current_node[1]

        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= crow + direction[0] < rows:
                if 0 <= ccol + direction[1] < cols:
                    if (crow + direction[0], ccol + direction[1]) not in obstacles:
                        frontier.append(
                            (
                                (crow + direction[0], ccol + direction[1]),
                                path + [(crow + direction[0], ccol + direction[1])],
                            )
                        )

    # No Path Found
    return []