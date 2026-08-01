
def sin(a):
    return prims.sin(a)


def sin(g: jit_utils.GraphContext, self):
    return g.op("Sin", self)


def sin(x):
    """evaluates the sine of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.sin(x))
    elif isinstance(x, interval):
        if not x.is_valid:
            return interval(-1, 1, is_valid=x.is_valid)
        na, __ = divmod(x.start, np.pi / 2.0)
        nb, __ = divmod(x.end, np.pi / 2.0)
        start = min(np.sin(x.start), np.sin(x.end))
        end = max(np.sin(x.start), np.sin(x.end))
        if nb - na > 4:
            return interval(-1, 1, is_valid=x.is_valid)
        elif na == nb:
            return interval(start, end, is_valid=x.is_valid)
        else:
            if (na - 1) // 4 != (nb - 1) // 4:
                #sin has max
                end = 1
            if (na - 3) // 4 != (nb - 3) // 4:
                #sin has min
                start = -1
            return interval(start, end)
    else:
        raise NotImplementedError


def sin(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SinOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def sin(src: _ods_ir.Value[_ods_ir.FloatType], *, ftz: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.FloatType]:
  return SinOp(src=src, ftz=ftz, results=results, loc=loc, ip=ip).result


def sin(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise sine: :math:`\mathrm{sin}(x)`.

  For floating-point inputs, this function lowers directly to the
  `stablehlo.sine`_ operation. For complex inputs, it lowers to a
  sequence of HLO operations implementing the complex sine.

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
    sine.

  See also:
    - :func:`jax.lax.cos`: elementwise cosine.
    - :func:`jax.lax.tan`: elementwise tangent.
    - :func:`jax.lax.asin`: elementwise arc sine.

  .. _stablehlo.sine: https://openxla.org/stablehlo/spec#sine
  """
  return sin_p.bind(x, accuracy=accuracy)


def sin(x: ArrayLike, /) -> Array:
  """Compute a trigonometric sine of each element of input.

  JAX implementation of :obj:`numpy.sin`.

  Args:
    x: array or scalar. Angle in radians.

  Returns:
    An array containing the sine of each element in ``x``, promotes to inexact
    dtype.

  See also:
    - :func:`jax.numpy.cos`: Computes a trigonometric cosine of each element of
      input.
    - :func:`jax.numpy.tan`: Computes a trigonometric tangent of each element of
      input.
    - :func:`jax.numpy.arcsin` and :func:`jax.numpy.asin`: Computes the inverse of
      trigonometric sine of each element of input.

  Examples:
    >>> pi = jnp.pi
    >>> x = jnp.array([pi/4, pi/2, 3*pi/4, pi])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   print(jnp.sin(x))
    [ 0.707  1.     0.707 -0.   ]
  """
  out = lax.sin(*promote_args_inexact('sin', x))
  jnp_error._set_error_if_nan(out)
  return out

