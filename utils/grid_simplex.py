
def grid_simplex(step=.1, boundary=False):
  """Generator for regular 'lattice' on the 2-simplex.

  Args:
    step: Defines spacing along one dimension.
    boundary: Include points on the boundary/face of the simplex.

  Yields:
    Next point on the grid.
  """
  eps = 1e-8
  start = 0. if boundary else step
  stop = 1. + eps if boundary else 1. - step + eps
  for a in np.arange(start, stop, step, dtype=np.double):
    for b in np.arange(start, stop - a, step, dtype=np.double):
      yield [a, b, 1. - a - b]

