
def tanh(x):
    return np.tanh(x)


def tanh(input):  # noqa: D400,D402
    r"""tanh(input) -> Tensor

    Applies element-wise,
    :math:`\text{Tanh}(x) = \tanh(x) = \frac{\exp(x) - \exp(-x)}{\exp(x) + \exp(-x)}`

    See :class:`~torch.nn.Tanh` for more details.
    """
    return input.tanh()


def tanh(a):
    return prims.tanh(a)


def tanh(g: jit_utils.GraphContext, self):
    return g.op("Tanh", self)


def tanh(x):
    """Evaluates the hyperbolic tan of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.tanh(x), np.tanh(x))
    elif isinstance(x, interval):
        return interval(np.tanh(x.start), np.tanh(x.end), is_valid=x.is_valid)
    else:
        raise NotImplementedError


def tanh(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TanhOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def tanh(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TanhOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def tanh(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TanhOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def tanh(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise hyperbolic tangent: :math:`\mathrm{tanh}(x)`.

  This function lowers directly to the `stablehlo.tanh`_ operation.

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
    hyperbolic tangent.

  See also:
    - :func:`jax.lax.atanh`: elementwise inverse hyperbolic tangent.
    - :func:`jax.lax.cosh`: elementwise hyperbolic cosine.
    - :func:`jax.lax.sinh`: elementwise hyperbolic sine.

  .. _stablehlo.tanh: https://openxla.org/stablehlo/spec#tanh
  """
  return tanh_p.bind(x, accuracy=accuracy)


def tanh(x: ArrayLike, /) -> Array:
  r"""Calculate element-wise hyperbolic tangent of input.

  JAX implementation of :obj:`numpy.tanh`.

  The hyperbolic tangent is defined by:

  .. math::

    tanh(x) = \frac{sinh(x)}{cosh(x)} = \frac{e^x - e^{-x}}{e^x + e^{-x}}

  Args:
    x: input array or scalar.

  Returns:
    An array containing the hyperbolic tangent of each element of ``x``, promoting
    to inexact dtype.

  Note:
    ``jnp.tanh`` is equivalent to computing ``-1j * jnp.tan(1j * x)``.

  See also:
    - :func:`jax.numpy.sinh`: Computes the element-wise hyperbolic sine of the input.
    - :func:`jax.numpy.cosh`: Computes the element-wise hyperbolic cosine of the
      input.
    - :func:`jax.numpy.arctanh`:  Computes the element-wise inverse of hyperbolic
      tangent of the input.

  Examples:
    >>> x = jnp.array([[-1, 0, 1],
    ...                [3, -2, 5]])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.tanh(x)
    Array([[-0.762,  0.   ,  0.762],
           [ 0.995, -0.964,  1.   ]], dtype=float32)
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   -1j * jnp.tan(1j * x)
    Array([[-0.762+0.j,  0.   -0.j,  0.762-0.j],
           [ 0.995-0.j, -0.964+0.j,  1.   -0.j]],      dtype=complex64, weak_type=True)

    For complex-valued input:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.tanh(2-5j)
    Array(1.031+0.021j, dtype=complex64, weak_type=True)
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   -1j * jnp.tan(1j * (2-5j))
    Array(1.031+0.021j, dtype=complex64, weak_type=True)
  """
  return lax.tanh(*promote_args_inexact('tanh', x))

