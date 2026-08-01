
def _expand_dims_like(x, target):
  """Expands the shape of `x` to match `target`'s shape by adding singleton dimensions."""
  return x.reshape(list(x.shape) + [1] * (target.ndim - x.ndim))


def _expand_dims_like(x, target):
    """Expands the shape of `x` to match `target`'s shape by adding singleton dimensions."""
    return x.reshape(list(x.shape) + [1] * (target.ndim - x.ndim))

