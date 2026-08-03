import re
import math


def angle(x: torch.Tensor) -> torch.Tensor:
    if x.is_complex():
        return torch.where(
            torch.isnan(x.real), float("nan"), torch.atan2(x.imag, x.real)
        )

    # when x is real number
    #   if x >= 0, return 0
    #   if x < 0, return pi
    #   if x is nan, return nan
    _, dtype = elementwise_dtypes(
        x,
        type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
    )
    pi = torch.scalar_tensor(math.pi, dtype=dtype, device=x.device)
    ret = torch.where(x < 0, pi, 0.0)
    return torch.where(torch.isnan(x), float("nan"), ret)


def angle(z: ArrayLike, deg=False):
    result = torch.angle(z)
    if deg:
        result = result * (180 / torch.pi)
    return result


def angle(z, deg=False):
    """
    Return the angle of the complex argument.

    Parameters
    ----------
    z : array_like
        A complex number or sequence of complex numbers.
    deg : bool, optional
        Return angle in degrees if True, radians if False (default).

    Returns
    -------
    angle : ndarray or scalar
        The counterclockwise angle from the positive real axis on the complex
        plane in the range ``(-pi, pi]``, with dtype as numpy.float64.

    See Also
    --------
    arctan2
    absolute

    Notes
    -----
    This function passes the imaginary and real parts of the argument to
    `arctan2` to compute the result; consequently, it follows the convention
    of `arctan2` when the magnitude of the argument is zero. See example.

    Examples
    --------
    >>> import numpy as np
    >>> np.angle([1.0, 1.0j, 1+1j])               # in radians
    array([ 0.        ,  1.57079633,  0.78539816]) # may vary
    >>> np.angle(1+1j, deg=True)                  # in degrees
    45.0
    >>> np.angle([0., -0., complex(0., -0.), complex(-0., -0.)])  # convention
    array([ 0.        ,  3.14159265, -0.        , -3.14159265])

    """
    z = asanyarray(z)
    if issubclass(z.dtype.type, _nx.complexfloating):
        zimag = z.imag
        zreal = z.real
    else:
        zimag = 0
        zreal = z

    a = arctan2(zimag, zreal)
    if deg:
        a *= 180 / pi
    return a


def angle(z: ArrayLike, deg: bool = False) -> Array:
  """Return the angle of a complex valued number or array.

  JAX implementation of :func:`numpy.angle`.

  Args:
    z: A complex number or an array of complex numbers.
    deg: Boolean. If ``True``, returns the result in degrees else returns
      in radians. Default is ``False``.

  Returns:
    An array of counterclockwise angle of each element of ``z``, with the same
    shape as ``z`` of dtype float.

  Examples:

    If ``z`` is a number

    >>> z1 = 2+3j
    >>> jnp.angle(z1)
    Array(0.98279375, dtype=float32, weak_type=True)

    If ``z`` is an array

    >>> z2 = jnp.array([[1+3j, 2-5j],
    ...                 [4-3j, 3+2j]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(jnp.angle(z2))
    [[ 1.25 -1.19]
     [-0.64  0.59]]

    If ``deg=True``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(jnp.angle(z2, deg=True))
    [[ 71.57 -68.2 ]
     [-36.87  33.69]]
  """
  z = util.ensure_arraylike('angle', z)
  re = ufuncs.real(z)
  im = ufuncs.imag(z)
  dtype = re.dtype
  if not issubdtype(dtype, np.inexact) or (
      issubdtype(z.dtype, np.floating) and np.ndim(z) == 0):
    dtype = dtypes.default_float_dtype()
    re = lax.convert_element_type(re, dtype)
    im = lax.convert_element_type(im, dtype)
  result = lax.atan2(im, re)
  return ufuncs.degrees(result) if deg else result

