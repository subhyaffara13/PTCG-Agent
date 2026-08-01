
def _build_point_grid(n_per_side: int) -> np.ndarray:
    """Generates a 2D grid of points evenly spaced in [0,1]x[0,1]."""
    offset = 1 / (2 * n_per_side)
    points_one_side = np.linspace(offset, 1 - offset, n_per_side)
    points_x = np.tile(points_one_side[None, :], (n_per_side, 1))
    points_y = np.tile(points_one_side[:, None], (1, n_per_side))
    points = np.stack([points_x, points_y], axis=-1).reshape(-1, 2)
    return points


def _build_point_grid(n_per_side: int) -> torch.Tensor:
    """Generates a 2D grid of points evenly spaced in [0,1]x[0,1]."""
    offset = 1 / (2 * n_per_side)
    points_one_side = torch.linspace(offset, 1 - offset, n_per_side)
    points_x = torch.tile(points_one_side[None, :], (n_per_side, 1))
    points_y = torch.tile(points_one_side[:, None], (1, n_per_side))
    points = torch.stack([points_x, points_y], dim=-1).reshape(-1, 2)
    return points


def _build_point_grid(n_per_side: int) -> torch.Tensor:
    """Generates a 2D grid of points evenly spaced in [0,1]x[0,1]."""
    offset = 1 / (2 * n_per_side)
    points_one_side = torch.linspace(offset, 1 - offset, n_per_side)
    points_x = torch.tile(points_one_side[None, :], (n_per_side, 1))
    points_y = torch.tile(points_one_side[:, None], (1, n_per_side))
    points = torch.stack([points_x, points_y], dim=-1).reshape(-1, 2)
    return points


def _build_point_grid(n_per_side: int) -> torch.Tensor:
    """Generates a 2D grid of points evenly spaced in [0,1]x[0,1]."""
    offset = 1 / (2 * n_per_side)
    points_one_side = torch.linspace(offset, 1 - offset, n_per_side)
    points_x = torch.tile(points_one_side[None, :], (n_per_side, 1))
    points_y = torch.tile(points_one_side[:, None], (1, n_per_side))
    points = torch.stack([points_x, points_y], dim=-1).reshape(-1, 2)
    return points

