
def exp2(a):
    return prims.exp2(a)


def exp2(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return Exp2Op(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def exp2(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise base-2 exponential: :math:`2^x`.

  This function is implemented in terms of the `stablehlo.exponential`_
  and `stablehlo.multiply`_ operations.

  Args:
    x: input array. Must have floating-point or complex type.
    accuracy: Optional `lax.Tolerance` or `lax.AccuracyMode` object that
      selects the implementation of the op based on the requested accuracy. If
      the implementation cannot satisfy the requested tolerance, the
      compiler will return an error. If mode is specified and there are no
      multiple implementations available, the default implementation will be
      used.

  Returns:
    Array of the same shape and dtype as ``x`` containing the element-wise
    base-2 exponential.

  See also:
    - :func:`jax.lax.exp`: elementwise exponentional: :math:`e^x`.
    - :func:`jax.lax.log`: elementwise natural logarithm: :math:`\mathrm{log}(x)`.

  .. _stablehlo.exponential: https://openxla.org/stablehlo/spec#exponential
  .. _stablehlo.multiply: https://openxla.org/stablehlo/spec#multiply
  """
  return exp2_p.bind(x, accuracy=accuracy)


def exp2(x: ArrayLike, /) -> Array:
  """Calculate element-wise base-2 exponential of input.

  JAX implementation of :obj:`numpy.exp2`.

  Args:
    x: input array or scalar

  Returns:
    An array containing the base-2 exponential of each element in ``x``, promotes
    to inexact dtype.

  See also:
    - :func:`jax.numpy.log2`: Calculates base-2 logarithm of each element of input.
    - :func:`jax.numpy.exp`: Calculates exponential of each element of the input.
    - :func:`jax.numpy.expm1`: Calculates :math:`e^x-1` of each element of the
      input.

  Examples:
    ``jnp.exp2`` follows the properties of the exponential such as :math:`2^{a+b}
    = 2^a * 2^b`.

    >>> x1 = jnp.array([2, -4, 3, -1])
    >>> x2 = jnp.array([-1, 3, -2, 3])
    >>> jnp.exp2(x1+x2)
    Array([2. , 0.5, 2. , 4. ], dtype=float32)
    >>> jnp.exp2(x1)*jnp.exp2(x2)
    Array([2. , 0.5, 2. , 4. ], dtype=float32)
  """
  x, = promote_args_inexact("exp2", x)
  return lax.exp2(x)

