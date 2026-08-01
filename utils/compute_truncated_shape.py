
def compute_truncated_shape(
    shape: tuple[int, ...],
    edge_items: tuple[int | None, ...],
) -> tuple[int, ...]:
  """Computes the shape of a truncated array.

  This can be used to estimate the size of an array visualization after it has
  been truncated by `infer_balanced_truncation`.

  Args:
    shape: The original array shape.
    edge_items: Number of edge items to keep along each axis.

  Returns:
    The shape of the truncated array.
  """
  return tuple(
      orig if edge is None else 2 * edge + 1
      for orig, edge in zip(shape, edge_items)
  )

