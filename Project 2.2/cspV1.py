def solve_CSP(input_dict):
    rows = input_dict["rows"]
    cols = input_dict["cols"]
    squares = input_dict["input_squares"]
    obstacles = input_dict["obstacles"]

    def create_empty_grid(rows, cols, obstacles):
        grid = [[None for _ in range(cols)] for _ in range(rows)]
        for r, c in obstacles:
            grid[r][c] = "Obstacle"
        return grid

    def can_place_square(grid, size, row, col):
        if row + size > rows or col + size > cols:
            return False
        for r in range(row, row + size):
            for c in range(col, col + size):
                if grid[r][c] is not None:
                    return False
        return True

    def place_square(grid, size, row, col):
        for r in range(row, row + size):
            for c in range(col, col + size):
                grid[r][c] = size

    def remove_square(grid, size, row, col):
        for r in range(row, row + size):
            for c in range(col, col + size):
                grid[r][c] = None

    def all_squares_used(squares):
        for size, count in squares.items():
            if count > 0:
                return False
        return True

    def backtrack(grid, squares, result):
        if all_squares_used(squares):
            return True
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] is None:
                    for size in sorted(squares.keys(), reverse=True):
                        if squares[size] > 0 and can_place_square(grid, size, row, col):
                            place_square(grid, size, row, col)
                            result.append((size, row, col))
                            squares[size] -= 1
                            if backtrack(grid, squares, result):
                                return True
                            remove_square(grid, size, row, col)
                            result.pop()
                            squares[size] += 1
                    if grid[row][col] is None:
                        return False
        return False

    grid = create_empty_grid(rows, cols, obstacles)
    result = []
    if backtrack(grid, squares, result):
        return result
    else:
        return []
