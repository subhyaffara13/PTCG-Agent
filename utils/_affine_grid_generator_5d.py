
def _affine_grid_generator_5d(theta: Tensor, size: list[int], align_corners: bool):
    n, _, d, h, w = size
    base_grid = _make_base_grid_5d(theta, d, h, w, align_corners=align_corners)
    # base_grid shape is (d, h, w, 4) and theta shape is (n, 3, 4)
    # We do manually a matrix multiplication which is faster than mm()
    # (d * h * w, 4, 1) * (n, 1, 4, 3) -> (n, h * w, 3)
    grid = (base_grid.view(-1, 4, 1) * theta.mT.unsqueeze(1)).sum(-2)
    return grid.view(n, d, h, w, 3)

