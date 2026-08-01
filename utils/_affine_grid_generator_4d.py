
def _affine_grid_generator_4d(theta: Tensor, size: list[int], align_corners: bool):
    n, _, h, w = size
    base_grid = _make_base_grid_4d(theta, h, w, align_corners=align_corners)
    # base_grid shape is (h, w, 3) and theta shape is (n, 2, 3)
    # We do manually a matrix multiplication which is faster than mm()
    # (h * w, 3, 1) * (n, 1, 3, 2) -> (n, h * w, 2)
    grid = (base_grid.view(-1, 3, 1) * theta.mT.unsqueeze(1)).sum(-2)
    return grid.view(n, h, w, 2)

