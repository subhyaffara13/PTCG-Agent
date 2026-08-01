
def check_scalar_conversion(arr: Array):
  if arr.ndim > 0:
    raise TypeError("Only scalar arrays can be converted to Python scalars; "
                    f"got {arr.ndim=}")

