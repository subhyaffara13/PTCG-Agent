
def around(a, decimals=0, out=None):
    """
    Round an array to the given number of decimals.

    `around` is an alias of `~numpy.round`.

    See Also
    --------
    ndarray.round : equivalent method
    round : alias for this function
    ceil, fix, floor, rint, trunc

    """
    return _wrapfunc(a, 'round', decimals=decimals, out=out)


def around(a: ArrayLike, decimals: int = 0, out: None = None) -> Array:
  """Alias of :func:`jax.numpy.round`"""
  return round(a, decimals, out)

