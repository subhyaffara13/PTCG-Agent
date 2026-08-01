
def cosh(a):
    return prims.cosh(a)


def cosh(x):
    """Evaluates the hyperbolic cos of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.cosh(x), np.cosh(x))
    elif isinstance(x, interval):
        #both signs
        if x.start < 0 and x.end > 0:
            end = max(np.cosh(x.start), np.cosh(x.end))
            return interval(1, end, is_valid=x.is_valid)
        else:
            #Monotonic
            start = np.cosh(x.start)
            end = np.cosh(x.end)
            return interval(start, end, is_valid=x.is_valid)
    else:
        raise NotImplementedError


def cosh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoshOp(operand=operand, results=results, loc=loc, ip=ip).result


def cosh(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoshOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def cosh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoshOp(operand=operand, results=results, loc=loc, ip=ip).result


def cosh(x: ArrayLike) -> Array:
  r"""Elementwise hyperbolic cosine: :math:`\mathrm{cosh}(x)`.

  This function lowers directly to the ``chlo.cosh`` operation.

  Args:
    x: input array. Must have floating-point or complex type.

  Returns:
    Array of the same shape and dtype as ``x`` containing the element-wise
    hyperbolic cosine.

  See also:
    - :func:`jax.lax.acosh`: elementwise inverse hyperbolic cosine.
    - :func:`jax.lax.sinh`: elementwise hyperbolic sine.
    - :func:`jax.lax.tanh`: elementwise hyperbolic tangent.
  """
  return cosh_p.bind(x)


def cosh(x: ArrayLike, /) -> Array:
  r"""Calculate element-wise hyperbolic cosine of input.

  JAX implementation of :obj:`numpy.cosh`.

  The hyperbolic cosine is defined by:

  .. math::

    cosh(x) = \frac{e^x + e^{-x}}{2}

  Args:
    x: input array or scalar.

  Returns:
    An array containing the hyperbolic cosine of each element of ``x``, promoting
    to inexact dtype.

  Note:
    ``jnp.cosh`` is equivalent to computing ``jnp.cos(1j * x)``.

  See also:
    - :func:`jax.numpy.sinh`: Computes the element-wise hyperbolic sine of the input.
    - :func:`jax.numpy.tanh`: Computes the element-wise hyperbolic tangent of the
      input.
    - :func:`jax.numpy.arccosh`:  Computes the element-wise inverse of hyperbolic
      cosine of the input.

  Examples:
    >>> x = jnp.array([[3, -1, 0],
    ...                [4, 7, -5]])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.cosh(x)
    Array([[ 10.068,   1.543,   1.   ],
           [ 27.308, 548.317,  74.21 ]], dtype=float32)
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.cos(1j * x)
    Array([[ 10.068+0.j,   1.543+0.j,   1.   +0.j],
           [ 27.308+0.j, 548.317+0.j,  74.21 +0.j]],      dtype=complex64, weak_type=True)

    For complex-valued input:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.cosh(5+1j)
    Array(40.096+62.44j, dtype=complex64, weak_type=True)
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.cos(1j * (5+1j))
    Array(40.096+62.44j, dtype=complex64, weak_type=True)
  """
  return lax.cosh(*promote_args_inexact('cosh', x))

