
def _get_axes():
    import matplotlib.pyplot as plt

    return plt.figure().gca()


def _get_axes(
    N: int, K: int, index: Index | None, columns: Index | None
) -> tuple[Index, Index]:
    # helper to create the axes as indexes
    # return axes or defaults

    if index is None:
        index = default_index(N)
    else:
        index = ensure_index(index)

    if columns is None:
        columns = default_index(K)
    else:
        columns = ensure_index(columns)
    return index, columns


def _get_axes(axes, mesh_shape):
  if not axes:
    return ()
  assert mesh_shape is not None
  # Sort wrt mesh axis names so order is deterministic and doesn't hang in McJAX
  return tuple(n for n, _ in mesh_shape if n in axes)

