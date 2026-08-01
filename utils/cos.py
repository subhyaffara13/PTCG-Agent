
def cos(a):
    return prims.cos(a)


def cos(g: jit_utils.GraphContext, self):
    return g.op("Cos", self)


def cos(x):
    """Evaluates the cos of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.sin(x))
    elif isinstance(x, interval):
        if not (np.isfinite(x.start) and np.isfinite(x.end)):
            return interval(-1, 1, is_valid=x.is_valid)
        na, __ = divmod(x.start, np.pi / 2.0)
        nb, __ = divmod(x.end, np.pi / 2.0)
        start = min(np.cos(x.start), np.cos(x.end))
        end = max(np.cos(x.start), np.cos(x.end))
        if nb - na > 4:
            #differ more than 2*pi
            return interval(-1, 1, is_valid=x.is_valid)
        elif na == nb:
            #in the same quadarant
            return interval(start, end, is_valid=x.is_valid)
        else:
            if (na) // 4 != (nb) // 4:
                #cos has max
                end = 1
            if (na - 2) // 4 != (nb - 2) // 4:
                #cos has min
                start = -1
            return interval(start, end, is_valid=x.is_valid)
    else:
        raise NotImplementedError


def cos(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CosOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def cos(src: _ods_ir.Value[_ods_ir.FloatType], *, ftz: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.FloatType]:
  return CosOp(src=src, ftz=ftz, results=results, loc=loc, ip=ip).result


def cos(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise cosine: :math:`\mathrm{cos}(x)`.

  For floating-point inputs, this function lowers directly to the
  `stablehlo.cosine`_ operation. For complex inputs, it lowers to a
  sequence of HLO operations implementing the complex cosine.

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
    cosine.

  See also:
    - :func:`jax.lax.sin`: elementwise sine.
    - :func:`jax.lax.tan`: elementwise tangent.
    - :func:`jax.lax.acos`: elementwise arc cosine.

  .. _stablehlo.cosine: https://openxla.org/stablehlo/spec#cosine
  """
  return cos_p.bind(x, accuracy=accuracy)


def cos(x: ArrayLike, /) -> Array:
  """Compute a trigonometric cosine of each element of input.

  JAX implementation of :obj:`numpy.cos`.

  Args:
    x: scalar or array. Angle in radians.

  Returns:
    An array containing the cosine of each element in ``x``, promotes to inexact
    dtype.

  See also:
    - :func:`jax.numpy.sin`: Computes a trigonometric sine of each element of input.
    - :func:`jax.numpy.tan`: Computes a trigonometric tangent of each element of
      input.
    - :func:`jax.numpy.arccos` and :func:`jax.numpy.acos`: Computes the inverse of
      trigonometric cosine of each element of input.

  Examples:
    >>> pi = jnp.pi
    >>> x = jnp.array([pi/4, pi/2, 3*pi/4, 5*pi/6])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   print(jnp.cos(x))
    [ 0.707 -0.    -0.707 -0.866]
  """
  out = lax.cos(*promote_args_inexact('cos', x))
  jnp_error._set_error_if_nan(out)
  return out

