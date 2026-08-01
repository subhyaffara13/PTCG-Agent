
def tan(a):
    return prims.tan(a)


def tan(g: jit_utils.GraphContext, self):
    return g.op("Tan", self)


def tan(x):
    """Evaluates the tan of an interval"""
    return sin(x) / cos(x)


def tan(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TanOp(operand=operand, results=results, loc=loc, ip=ip).result


def tan(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TanOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def tan(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TanOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def tan(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TanOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def tan(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise tangent: :math:`\mathrm{tan}(x)`.

  This function lowers directly to the `stablehlo.tangent`_ operation.

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
    tangent.

  See also:
    - :func:`jax.lax.cos`: elementwise cosine.
    - :func:`jax.lax.sin`: elementwise sine.
    - :func:`jax.lax.atan`: elementwise arc tangent.
    - :func:`jax.lax.atan2`: elementwise 2-term arc tangent.

  .. _stablehlo.tangent: https://openxla.org/stablehlo/spec#tangent
  """
  return tan_p.bind(x, accuracy=accuracy)


def tan(x: ArrayLike, /) -> Array:
  """Compute a trigonometric tangent of each element of input.

  JAX implementation of :obj:`numpy.tan`.

  Args:
    x: scalar or array. Angle in radians.

  Returns:
    An array containing the tangent of each element in ``x``, promotes to inexact
    dtype.

  See also:
    - :func:`jax.numpy.sin`: Computes a trigonometric sine of each element of input.
    - :func:`jax.numpy.cos`: Computes a trigonometric cosine of each element of
      input.
    - :func:`jax.numpy.arctan` and :func:`jax.numpy.atan`: Computes the inverse of
      trigonometric tangent of each element of input.

  Examples:
    >>> pi = jnp.pi
    >>> x = jnp.array([0, pi/6, pi/4, 3*pi/4, 5*pi/6])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   print(jnp.tan(x))
    [ 0.     0.577  1.    -1.    -0.577]
  """
  out = lax.tan(*promote_args_inexact('tan', x))
  jnp_error._set_error_if_nan(out)
  return out

