
def grid_sampler_3d(
    input,
    grid,
    interpolation_mode,
    padding_mode,
    align_corners,
):
    check_grid_sampler_common(input, grid)
    check_grid_sampler_3d(input, grid, interpolation_mode)
    N = input.shape[0]
    C = input.shape[1]
    out_D = grid.shape[1]
    out_H = grid.shape[2]
    out_W = grid.shape[3]
    return input.new_empty((N, C, out_D, out_H, out_W))

