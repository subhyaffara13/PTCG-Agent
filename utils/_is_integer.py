
def _is_integer(x) -> bool:
    r"""Type check the input number is an integer.

    Will return True for int, SymInt, Numpy integers and Tensors with integer elements.
    """
    if isinstance(x, (int, torch.SymInt)):
        return True
    if np is not None and isinstance(x, np.integer):
        return True
    return isinstance(x, Tensor) and not x.is_floating_point()


def _is_integer(dtype: _NpDType) -> bool:
  """Validate the dtype is integer."""
  return np.issubdtype(dtype, np.integer)

