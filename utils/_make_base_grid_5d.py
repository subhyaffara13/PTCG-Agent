
def _make_base_grid_5d(theta: Tensor, d: int, h: int, w: int, align_corners: bool):
    dtype = theta.dtype
    device = theta.device

    grid_x = _linspace_from_neg_one(w, align_corners, dtype, device).view(1, 1, w, 1)
    grid_y = _linspace_from_neg_one(h, align_corners, dtype, device).view(1, h, 1, 1)
    grid_z = _linspace_from_neg_one(d, align_corners, dtype, device).view(d, 1, 1, 1)
    grid_one = torch.ones((1, 1, 1, 1), dtype=dtype, device=device)

    # this is just a temporary hack and we should use torch.stack here once #104480 is merged
    grid_x = torch.nn.functional.pad(grid_x, pad=(0, 3), mode="constant", value=0)
    grid_y = torch.nn.functional.pad(grid_y, pad=(1, 2), mode="constant", value=0)
    grid_z = torch.nn.functional.pad(grid_z, pad=(2, 1), mode="constant", value=0)
    grid_one = torch.nn.functional.pad(grid_one, pad=(3, 0), mode="constant", value=0)
    return grid_x + grid_y + grid_z + grid_one

