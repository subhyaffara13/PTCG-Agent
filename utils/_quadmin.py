
def _quadmin(a, fa, fpa, b, fb):
    """
    Finds the minimizer for a quadratic polynomial that goes through
    the points (a,fa), (b,fb) with derivative at a of fpa.

    """
    # f(x) = B*(x-a)^2 + C*(x-a) + D
    with np.errstate(divide='raise', over='raise', invalid='raise'):
        try:
            D = fa
            C = fpa
            db = b - a * 1.0
            B = (fb - D - C * db) / (db * db)
            xmin = a - C / (2.0 * B)
        except ArithmeticError:
            return None
    if not np.isfinite(xmin):
        return None
    return xmin


def _quadmin(a, fa, fpa, b, fb):
  """Quadratic interpolation.

  Finds a critical point of a quadratic polynomial
  p(x) = B*(x-a)^2 + C*(x-a) + D, that goes through
  the points (a,fa), (b,fb) with derivative at a of fpa.
  Adapted from scipy.optimize._linesearch.py.

  Args:
    a: scalar
    fa: value of a function f at a
    fpa: slope of a function f at a
    b: scalar
    fb: value of a function f at b

  Returns:
    xmin: point at which p'(xmin) = 0
  """
  D = fa
  C = fpa
  db = b - a
  B = (fb - D - C * db) / (db**2)
  xmin = a - C / (2.0 * B)
  return xmin


def _quadmin(a, fa, fpa, b, fb):
  D = fa
  C = fpa
  db = b - a
  B = (fb - D - C * db) / (db ** 2)
  xmin = a - C / (2. * B)
  return xmin

