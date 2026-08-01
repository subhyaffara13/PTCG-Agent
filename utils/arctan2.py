
def arctan2(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  r"""Compute the arctangent of x1/x2, choosing the correct quadrant.

  JAX implementation of :func:`numpy.arctan2`

  Args:
    x1: numerator array.
    x2: denomniator array; should be broadcast-compatible with x1.

  Returns:
    The elementwise arctangent of x1 / x2, tracking the correct quadrant.

  See also:
    - :func:`jax.numpy.tan`: compute the tangent of an angle
    - :func:`jax.numpy.atan2`: the array API version of this function.

  Examples:
    Consider a sequence of angles in radians between 0 and :math:`2\pi`:

    >>> theta = jnp.linspace(-jnp.pi, jnp.pi, 9)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(theta)
    [-3.14 -2.36 -1.57 -0.79  0.    0.79  1.57  2.36  3.14]

    These angles can equivalently be represented by ``(x, y)`` coordinates
    on a unit circle:

    >>> x, y = jnp.cos(theta), jnp.sin(theta)

    To reconstruct the input angle, we might be tempted to use the identity
    :math:`\tan(\theta) = y / x`, and compute :math:`\theta = \tan^{-1}(y/x)`.
    Unfortunately, this does not recover the input angle:

    >>> with jnp.printoptions(precision=2, suppress=True):  # doctest: +SKIP
    ...   print(jnp.arctan(y / x))
    [-0.    0.79  1.57 -0.79  0.    0.79  1.57 -0.79  0.  ]

    The problem is that :math:`y/x` contains some ambiguity: although
    :math:`(y, x) = (-1, -1)` and :math:`(y, x) = (1, 1)` represent different points in
    Cartesian space, in both cases :math:`y / x = 1`, and so the simple arctan
    approach loses information about which quadrant the angle lies in. :func:`arctan2`
    is built to address this:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...  print(jnp.arctan2(y, x))
    [ 3.14 -2.36 -1.57 -0.79  0.    0.79  1.57  2.36 -3.14]

    The results match the input ``theta``, except at the endpoints where :math:`+\pi`
    and :math:`-\pi` represent indistinguishable points on the unit circle. By convention,
    :func:`arctan2` always returns values between :math:`-\pi` and :math:`+\pi` inclusive.
  """
  return lax.atan2(*promote_args_inexact("arctan2", x1, x2))

