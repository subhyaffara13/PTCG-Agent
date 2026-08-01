
def _expect(fun, lb, ub, x0, inc, maxcount=1000, tolerance=1e-10,
            chunksize=32):
    """Helper for computing the expectation value of `fun`."""
    # short-circuit if the support size is small enough
    if (ub - lb) <= chunksize:
        supp = np.arange(lb, ub+1, inc)
        vals = fun(supp)
        return np.sum(vals)

    # otherwise, iterate starting from x0
    if x0 < lb:
        x0 = lb
    if x0 > ub:
        x0 = ub

    count, tot = 0, 0.
    # iterate over [x0, ub] inclusive
    for x in _iter_chunked(x0, ub+1, chunksize=chunksize, inc=inc):
        count += x.size
        delta = np.sum(fun(x))
        tot += delta
        if abs(delta) < tolerance * x.size:
            break
        if count > maxcount:
            warnings.warn('expect(): sum did not converge',
                          RuntimeWarning, stacklevel=3)
            return tot

    # iterate over [lb, x0)
    for x in _iter_chunked(x0-1, lb-1, chunksize=chunksize, inc=-inc):
        count += x.size
        delta = np.sum(fun(x))
        tot += delta
        if abs(delta) < tolerance * x.size:
            break
        if count > maxcount:
            warnings.warn('expect(): sum did not converge',
                          RuntimeWarning, stacklevel=3)
            break

    return tot


def _expect(controller, expected):
  """Reads a line from the controller, checks it matches expected line exactly."""
  line = controller.read_line()
  if expected != line:
    raise ValueError("Received '{}' but expected '{}'".format(line, expected))


def _expect(client, expected):
  """Reads a line from the client, checks it matches expected line exactly."""
  line = client.read_line()
  if expected != line:
    raise ValueError("Received '{}' but expected '{}'".format(line, expected))

