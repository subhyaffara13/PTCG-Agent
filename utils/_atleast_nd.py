
def _atleast_nd(a, ndim):
    # Ensures `a` has at least `ndim` dimensions by prepending
    # ones to `a.shape` as necessary
    return array(a, ndmin=ndim, copy=None, subok=True)


def _atleast_nd(x: ArrayLike, n: int) -> Array:
  m = np.ndim(x)
  return lax.broadcast(x, (1,) * (n - m)) if m < n else asarray(x)

