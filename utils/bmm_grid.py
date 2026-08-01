
def bmm_grid(b, m, n, meta, *, cdiv, max):
    tiles = cdiv(m, meta["BLOCK_M"]) * cdiv(n, meta["BLOCK_N"])
    # Split batch across grid_y and grid_z to avoid exceeding CUDA grid_y limit.
    # When b <= max_y_grid, grid_z = 1 and behavior is identical to the original.
    max_y_grid = get_max_y_grid()
    grid_z = max(cdiv(b, max_y_grid), 1)
    grid_y = cdiv(b, grid_z)
    return (tiles, grid_y, grid_z)

