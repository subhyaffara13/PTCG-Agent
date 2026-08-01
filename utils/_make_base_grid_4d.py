
def _make_base_grid_4d(theta: Tensor, h: int, w: int, align_corners: bool):
    dtype = theta.dtype
    device = theta.device

    # Using padding and summation generates a single kernel vs using torch.stack where 3 kernels generated
    # corresponding to each individual tensor: grid_x, grid_y, grid_one
    grid_x = _linspace_from_neg_one(w, align_corners, dtype, device).view(1, w, 1)
    grid_y = _linspace_from_neg_one(h, align_corners, dtype, device).view(h, 1, 1)
    grid_one = torch.ones((1, 1, 1), dtype=dtype, device=device)

    # this is just a temporary hack and we should use torch.stack here once #104480 is merged
    grid_x = torch.nn.functional.pad(grid_x, pad=(0, 2), mode="constant", value=0)
    grid_y = torch.nn.functional.pad(grid_y, pad=(1, 1), mode="constant", value=0)
    grid_one = torch.nn.functional.pad(grid_one, pad=(2, 0), mode="constant", value=0)
    return grid_x + grid_y + grid_one

