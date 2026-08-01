
def _is_mlx(x):
    import mlx.core as mx

    return isinstance(x, mx.array)

