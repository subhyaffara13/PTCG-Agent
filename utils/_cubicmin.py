
def _cubicmin(a, fa, fpa, b, fb, c, fc):
    """
    Finds the minimizer for a cubic polynomial that goes through the
    points (a,fa), (b,fb), and (c,fc) with derivative at a of fpa.

    If no minimizer can be found, return None.

    """
    # f(x) = A *(x-a)^3 + B*(x-a)^2 + C*(x-a) + D

    with np.errstate(divide='raise', over='raise', invalid='raise'):
        try:
            C = fpa
            db = b - a
            dc = c - a
            denom = (db * dc) ** 2 * (db - dc)
            d1 = np.empty((2, 2))
            d1[0, 0] = dc ** 2
            d1[0, 1] = -db ** 2
            d1[1, 0] = -dc ** 3
            d1[1, 1] = db ** 3
            [A, B] = np.dot(d1, np.asarray([fb - fa - C * db,
                                            fc - fa - C * dc]).flatten())
            A /= denom
            B /= denom
            radical = B * B - 3 * A * C
            xmin = a + (-B + np.sqrt(radical)) / (3 * A)
        except ArithmeticError:
            return None
    if not np.isfinite(xmin):
        return None
    return xmin


def _cubicmin(a, fa, fpa, b, fb, c, fc):
  """Cubic interpolation.

  Finds a critical point of a cubic polynomial
  p(x) = A *(x-a)^3 + B*(x-a)^2 + C*(x-a) + D, that goes through
  the points (a,fa), (b,fb), and (c,fc) with derivative at a of fpa.
  May return NaN (if radical<0), in that case, the point will be ignored.
  Adapted from scipy.optimize._linesearch.py.

  Args:
    a: scalar
    fa: value of a function f at a
    fpa: slope of a function f at a
    b: scalar
    fb: value of a function f at b
    c: scalar
    fc: value of a function f at c

  Returns:
    xmin: point at which p'(xmin) = 0
  """
  C = fpa
  db = b - a
  dc = c - a
  denom = (db * dc) ** 2 * (db - dc)
  d1 = jnp.array([[dc**2, -(db**2)], [-(dc**3), db**3]])
  A, B = (
      jnp.dot(
          d1,
          jnp.array([fb - fa - C * db, fc - fa - C * dc]),
          precision=jax.lax.Precision.HIGHEST,
      )
      / denom
  )

  radical = B * B - 3.0 * A * C
  xmin = a + (-B + jnp.sqrt(radical)) / (3.0 * A)

  return xmin


def _cubicmin(a, fa, fpa, b, fb, c, fc):
  dtype = dtypes.result_type(a, fa, fpa, b, fb, c, fc)
  C = fpa
  db = b - a
  dc = c - a
  denom = (db * dc) ** 2 * (db - dc)
  d1 = jnp.array([[dc ** 2, -db ** 2],
                  [-dc ** 3, db ** 3]], dtype=dtype)
  d2 = jnp.array([fb - fa - C * db, fc - fa - C * dc], dtype=dtype)
  A, B = _dot(d1, d2) / denom

  radical = B * B - 3. * A * C
  xmin = a + (-B + jnp.sqrt(radical)) / (3. * A)

  return xmin

