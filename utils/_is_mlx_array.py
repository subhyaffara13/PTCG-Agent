import sys

def _is_mlx_array(x):
    """Return whether *x* is a MLX Array."""
    try:
        # We're intentionally not attempting to import mlx. If somebody
        # has created a mlx array, mlx should already be in sys.modules.
        tp = sys.modules.get("mlx.core").array
    except AttributeError:
        return False  # Module not imported or a nonstandard module with no Array attr.
    return (isinstance(tp, type)  # Just in case it's a very nonstandard module.
            and isinstance(x, tp))

