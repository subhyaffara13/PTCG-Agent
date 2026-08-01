
def is_mlx_array(x) -> bool:
    """
    Tests if `x` is a mlx array or not. Safe to call even when mlx is not installed.
    """
    return False if not _is_mlx_available else _is_mlx(x)

