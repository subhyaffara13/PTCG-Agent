
def split_image_into_grid(h: int, w: int, grid: tuple[int, int]) -> list[tuple[int, int, int, int]]:
    row_height = h // grid[0]
    col_width = w // grid[1]
    return [
        (
            col * col_width,
            row * row_height,
            w if col == grid[1] - 1 else (col + 1) * col_width,
            h if row == grid[0] - 1 else (row + 1) * row_height,
        )
        for row in range(grid[0])
        for col in range(grid[1])
    ]


def split_image_into_grid(h: int, w: int, grid: tuple[int, int]) -> list[tuple[int, int, int, int]]:
    row_height = h // grid[0]
    col_width = w // grid[1]
    return [
        (
            col * col_width,
            row * row_height,
            w if col == grid[1] - 1 else (col + 1) * col_width,
            h if row == grid[0] - 1 else (row + 1) * row_height,
        )
        for row in range(grid[0])
        for col in range(grid[1])
    ]

