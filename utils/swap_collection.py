
def swap_collection(fn: Callable[..., Any], col_a: str, col_b: str):
  """Swap two collections."""

  def swap(target):
    a = target[col_a] if col_a in target else {}
    b = target[col_b] if col_b in target else {}
    target[col_b], target[col_a] = a, b
    return target

  return map_variables(fn, (col_a, col_b), swap, swap, mutable=True)

