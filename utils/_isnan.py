
def _isnan(val):
    try:
        return val is not pd.NA and np.isnan(val)
    except TypeError:
        return False


def _isnan(x: ArrayLike) -> Array:
  return ne(x, x)


def _isnan(x: ArrayLike) -> Array:
  return lax.ne(x, x)

