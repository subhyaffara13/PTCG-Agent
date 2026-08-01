
def sinh(a):
    return prims.sinh(a)


def sinh(x):
    """Evaluates the hyperbolic sine of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.sinh(x), np.sinh(x))
    elif isinstance(x, interval):
        return interval(np.sinh(x.start), np.sinh(x.end), is_valid=x.is_valid)
    else:
        raise NotImplementedError


def sinh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SinhOp(operand=operand, results=results, loc=loc, ip=ip).result


def sinh(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SinhOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def sinh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SinhOp(operand=operand, results=results, loc=loc, ip=ip).result


def sinh(x: ArrayLike) -> Array:
  r"""Elementwise hyperbolic sine: :math:`\mathrm{sinh}(x)`.

  This function lowers directly to the ``chlo.sinh`` operation.

  Args:
    x: input array. Must have floating-point or complex type.

  Returns:
    Array of the same shape and dtype as ``x`` containing the element-wise
    hyperbolic sine.

  See also:
    - :func:`jax.lax.asinh`: elementwise inverse hyperbolic sine.
    - :func:`jax.lax.cosh`: elementwise hyperbolic cosine.
    - :func:`jax.lax.tanh`: elementwise hyperbolic tangent.
  """
  return sinh_p.bind(x)


def sinh(x: ArrayLike, /) -> Array:
  r"""Calculate element-wise hyperbolic sine of input.

  JAX implementation of :obj:`numpy.sinh`.

  The hyperbolic sine is defined by:

  .. math::

    sinh(x) = \frac{e^x - e^{-x}}{2}

  Args:
    x: input array or scalar.

  Returns:
    An array containing the hyperbolic sine of each element of ``x``, promoting
    to inexact dtype.

  Note:
    ``jnp.sinh`` is equivalent to computing ``-1j * jnp.sin(1j * x)``.

  See also:
    - :func:`jax.numpy.cosh`: Computes the element-wise hyperbolic cosine of the
      input.
    - :func:`jax.numpy.tanh`: Computes the element-wise hyperbolic tangent of the
      input.
    - :func:`jax.numpy.arcsinh`:  Computes the element-wise inverse of hyperbolic
      sine of the input.

  Examples:
    >>> x = jnp.array([[-2, 3, 5],
    ...                [0, -1, 4]])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.sinh(x)
    Array([[-3.627, 10.018, 74.203],
           [ 0.   , -1.175, 27.29 ]], dtype=float32)
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   -1j * jnp.sin(1j * x)
    Array([[-3.627+0.j, 10.018-0.j, 74.203-0.j],
           [ 0.   -0.j, -1.175+0.j, 27.29 -0.j]],      dtype=complex64, weak_type=True)

    For complex-valued input:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.sinh(3-2j)
    Array(-4.169-9.154j, dtype=complex64, weak_type=True)
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   -1j * jnp.sin(1j * (3-2j))
    Array(-4.169-9.154j, dtype=complex64, weak_type=True)
  """
  return lax.sinh(*promote_args_inexact('sinh', x))

