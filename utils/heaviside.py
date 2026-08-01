
def heaviside(input: TensorLikeType, values: TensorLikeType) -> TensorLikeType:
    input_eq_zero = torch.eq(input, 0)
    input_lt_zero = torch.logical_or(torch.lt(input, 0), torch.isnan(input))
    zeros_and_ones = torch.where(input_lt_zero, 0, 1)
    output = torch.where(input_eq_zero, values, zeros_and_ones)
    return output


def heaviside(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  r"""Compute the heaviside step function.

  JAX implementation of :obj:`numpy.heaviside`.

  The heaviside step function is defined by:

  .. math::

    \mathrm{heaviside}(x1, x2) = \begin{cases}
      0,  & x1 < 0\\
      x2, & x1 = 0\\
      1,  & x1 > 0.
    \end{cases}

  Args:
    x1: input array or scalar. ``complex`` dtype are not supported.
    x2: scalar or array. Specifies the return values when ``x1`` is ``0``. ``complex``
      dtype are not supported. ``x1`` and ``x2`` must either have same shape or
      broadcast compatible.

  Returns:
    An array containing the heaviside step function of ``x1``, promoting to
    inexact dtype.

  Examples:
    >>> x1 = jnp.array([[-2, 0, 3],
    ...                 [5, -1, 0],
    ...                 [0, 7, -3]])
    >>> x2 = jnp.array([2, 0.5, 1])
    >>> jnp.heaviside(x1, x2)
    Array([[0. , 0.5, 1. ],
           [1. , 0. , 1. ],
           [2. , 1. , 0. ]], dtype=float32)
    >>> jnp.heaviside(x1, 0.5)
    Array([[0. , 0.5, 1. ],
           [1. , 0. , 0.5],
           [0.5, 1. , 0. ]], dtype=float32)
    >>> jnp.heaviside(-3, x2)
    Array([0., 0., 0.], dtype=float32)
  """
  x1, x2 = ensure_arraylike("heaviside", x1, x2)
  x1, x2 = promote_dtypes_inexact(x1, x2)
  zero = _lax_const(x1, 0)
  return _where(lax.lt(x1, zero), zero,
                _where(lax.gt(x1, zero), _lax_const(x1, 1),
                       _where(lax._isnan(x1), x1, x2)))

