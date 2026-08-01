
def hypot(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.hypot(a, b)


def hypot(x1, x2):
    if not USE_NAIVE_MATH:
        return np.hypot(x1, x2)
    if not np.isfinite(x1):
        r = abs(x1)
    elif not np.isfinite(x2):
        r = abs(x2)
    else:
        y = abs(np.array([x1, x2]))
        y = np.array([min(y), max(y)])
        if y[0] > np.sqrt(REALMIN) and y[1] < np.sqrt(REALMAX/2.1):
            r = np.sqrt(sum(y*y))
        elif y[1] > 0:
            r = y[1] * np.sqrt((y[0]/y[1])*(y[0]/y[1]) + 1)
        else:
            r = 0
    return r


def hypot(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  r"""
  Return element-wise hypotenuse for the given legs of a right angle triangle.

  JAX implementation of :obj:`numpy.hypot`.

  Args:
    x1: scalar or array. Specifies one of the legs of right angle triangle.
      ``complex`` dtype are not supported.
    x2: scalar or array. Specifies the other leg of right angle triangle.
      ``complex`` dtype are not supported. ``x1`` and ``x2`` must either have
      same shape or be broadcast compatible.

  Returns:
    An array containing the hypotenuse for the given given legs ``x1`` and ``x2``
    of a right angle triangle, promoting to inexact dtype.

  Note:
    ``jnp.hypot`` is a more numerically stable way of computing
    ``jnp.sqrt(x1 ** 2 + x2 **2)``.

  Examples:
    >>> jnp.hypot(3, 4)
    Array(5., dtype=float32, weak_type=True)
    >>> x1 = jnp.array([[3, -2, 5],
    ...                 [9, 1, -4]])
    >>> x2 = jnp.array([-5, 6, 8])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.hypot(x1, x2)
    Array([[ 5.831,  6.325,  9.434],
           [10.296,  6.083,  8.944]], dtype=float32)
  """
  x1, x2 = promote_args_inexact("hypot", x1, x2)

  # TODO(micky774): Promote to ValueError when deprecation is complete
  # (began 2024-4-14).
  if dtypes.issubdtype(x1.dtype, np.complexfloating):
    raise ValueError(
      "jnp.hypot is not well defined for complex-valued inputs. "
      "Please convert to real values first, such as by using abs(x)")
  x1, x2 = lax.abs(x1), lax.abs(x2)
  idx_inf = lax.bitwise_or(isposinf(x1), isposinf(x2))
  x1, x2 = maximum(x1, x2), minimum(x1, x2)
  x = _where(x1 == 0, x1, x1 * lax.sqrt(1 + lax.square(lax.div(x2, _where(x1 == 0, lax._ones(x1), x1)))))
  return _where(idx_inf, _lax_const(x, np.inf), x)

