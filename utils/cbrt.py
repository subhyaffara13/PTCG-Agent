
def cbrt(x):
    return torch.pow(x, 1 / 3)


def cbrt(arg, evaluate=None):
    """Returns the principal cube root.

    Parameters
    ==========

    evaluate : bool, optional
        The parameter determines if the expression should be evaluated.
        If ``None``, its value is taken from
        ``global_parameters.evaluate``.

    Examples
    ========

    >>> from sympy import cbrt, Symbol
    >>> x = Symbol('x')

    >>> cbrt(x)
    x**(1/3)

    >>> cbrt(x)**3
    x

    Note that cbrt(x**3) does not simplify to x.

    >>> cbrt(x**3)
    (x**3)**(1/3)

    This is because the two are not equal to each other in general.
    For example, consider `x == -1`:

    >>> from sympy import Eq
    >>> Eq(cbrt(x**3), x).subs(x, -1)
    False

    This is because cbrt computes the principal cube root, this
    identity does hold if `x` is positive:

    >>> y = Symbol('y', positive=True)
    >>> cbrt(y**3)
    y

    See Also
    ========

    sympy.polys.rootoftools.rootof, root, real_root

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Cube_root
    .. [2] https://en.wikipedia.org/wiki/Principal_value

    """
    return Pow(arg, Rational(1, 3), evaluate=evaluate)


def cbrt(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CbrtOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def cbrt(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CbrtOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def cbrt(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CbrtOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def cbrt(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise cube root: :math:`\sqrt[3]{x}`.

  This function lowers directly to the `stablehlo.cbrt`_ operation.

  Args:
    x: Input array. Must have floating or complex dtype.
    accuracy: Optional `lax.Tolerance` or `lax.AccuracyMode` object that
      selects the implementation of the op based on the requested accuracy. If
      the implementation cannot satisfy the requested tolerance, the
      compiler will return an error. If mode is specified and there are no
      multiple implementations available, the default implementation will be
      used.

  Returns:
    An array of the same shape and dtype as ``x`` containing the cube root.

  See also:
    :func:`jax.lax.pow`: Elementwise power.
    :func:`jax.lax.sqrt`: Elementwise square root.
    :func:`jax.lax.rsqrt`: Elementwise reciporical square root.

  .. _stablehlo.cbrt: https://openxla.org/stablehlo/spec#cbrt
  """
  return cbrt_p.bind(x, accuracy=accuracy)


def cbrt(x: ArrayLike, /) -> Array:
  """Calculates element-wise cube root of the input array.

  JAX implementation of :obj:`numpy.cbrt`.

  Args:
    x: input array or scalar. ``complex`` dtypes are not supported.

  Returns:
    An array containing the cube root of the elements of ``x``.

  See also:
    - :func:`jax.numpy.sqrt`: Calculates the element-wise non-negative square root
      of the input.
    - :func:`jax.numpy.square`: Calculates the element-wise square of the input.

  Examples:
    >>> x = jnp.array([[216, 125, 64],
    ...                [-27, -8, -1]])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.cbrt(x)
    Array([[ 6.,  5.,  4.],
           [-3., -2., -1.]], dtype=float32)
  """
  return lax.cbrt(*promote_args_inexact('cbrt', x))

