
def _ensure_str(name):
    """
    Ensure that an index / column name is a str (python 3); otherwise they
    may be np.string dtype. Non-string dtypes are passed through unchanged.

    https://github.com/pandas-dev/pandas/issues/13492
    """
    if isinstance(name, str):
        name = str(name)
    return name


def _ensure_str(x: str) -> str:
  if not isinstance(x, str):
    raise TypeError(f"argument is not a string: {x}")
  return x

