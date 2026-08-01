
def _scan_nd(body_fn, init, xs, n=1, unroll=(1,)):
  """Utility for performing an n-dimensional `lax.scan`.

  The n-d scan is simply recursive call of 1-d scan.
  Args:
    body_fn: the body of the loop of type (c, x) -> (c, y).
    init: initial value for the carry.
    xs: a pytree of tensors to scan over.
    n: number of dimensions to scan over (default: 1)
  Returns:
    A tuple of the final carry and the values returned by the body.
  """
  if n == 1:
    return lax.scan(body_fn, init, xs, unroll=unroll[0])
  else:

    def scan_body(c, x):
      return _scan_nd(body_fn, c, x, n=n - 1, unroll=unroll[1:])

    return lax.scan(scan_body, init, xs, unroll=unroll[0])

