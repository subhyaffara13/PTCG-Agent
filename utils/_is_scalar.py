
def _is_scalar(e):
    """ Helper method used in Tr"""

    # sympify to set proper attributes
    e = sympify(e)
    if isinstance(e, Expr):
        if (e.is_Integer or e.is_Float or
            e.is_Rational or e.is_Number or
            (e.is_Symbol and e.is_commutative)
                ):
            return True

    return False


def _is_scalar(value, stringlike=(str, bytes)):
    "Scalars are bytes, strings, and non-iterables."
    try:
        iter(value)
    except TypeError:
        return True
    return isinstance(value, stringlike)


def _is_scalar(arr):
  return isinstance(arr, (ScalarType, np.number))


def _is_scalar(x):
  """Checks if a Python or NumPy scalar."""
  return np.isscalar(x) or (
      isinstance(x, (np.ndarray, Array))
      and np.ndim(x) == 0
  )

