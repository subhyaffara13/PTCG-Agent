
def sqrt(a):
    return prims.sqrt(a)


def sqrt(g: jit_utils.GraphContext, self):
    if _type_utils.JitScalarType.from_value(
        self, _type_utils.JitScalarType.UNDEFINED
    ) in {
        _type_utils.JitScalarType.UINT8,
        _type_utils.JitScalarType.INT8,
        _type_utils.JitScalarType.INT16,
        _type_utils.JitScalarType.INT,
        _type_utils.JitScalarType.INT64,
    }:
        # torch converts all int inputs to sqrt to float
        self = g.op("Cast", self, to_i=_C_onnx.TensorProtoDataType.FLOAT)

    return g.op("Sqrt", self)


def sqrt(x):
    """Integer square root of x."""
    return int(mlib.isqrt(int(x)))


def sqrt(x):
    """Evaluates the square root of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        if x > 0:
            return interval(np.sqrt(x))
        else:
            return interval(-np.inf, np.inf, is_valid=False)
    elif isinstance(x, interval):
        #Outside the domain
        if x.end < 0:
            return interval(-np.inf, np.inf, is_valid=False)
        #Partially outside the domain
        elif x.start < 0:
            return interval(-np.inf, np.inf, is_valid=None)
        else:
            return interval(np.sqrt(x.start), np.sqrt(x.end),
                    is_valid=x.is_valid)
    else:
        raise NotImplementedError


def sqrt(arg, evaluate=None):
    """Returns the principal square root.

    Parameters
    ==========

    evaluate : bool, optional
        The parameter determines if the expression should be evaluated.
        If ``None``, its value is taken from
        ``global_parameters.evaluate``.

    Examples
    ========

    >>> from sympy import sqrt, Symbol, S
    >>> x = Symbol('x')

    >>> sqrt(x)
    sqrt(x)

    >>> sqrt(x)**2
    x

    Note that sqrt(x**2) does not simplify to x.

    >>> sqrt(x**2)
    sqrt(x**2)

    This is because the two are not equal to each other in general.
    For example, consider x == -1:

    >>> from sympy import Eq
    >>> Eq(sqrt(x**2), x).subs(x, -1)
    False

    This is because sqrt computes the principal square root, so the square may
    put the argument in a different branch.  This identity does hold if x is
    positive:

    >>> y = Symbol('y', positive=True)
    >>> sqrt(y**2)
    y

    You can force this simplification by using the powdenest() function with
    the force option set to True:

    >>> from sympy import powdenest
    >>> sqrt(x**2)
    sqrt(x**2)
    >>> powdenest(sqrt(x**2), force=True)
    x

    To get both branches of the square root you can use the rootof function:

    >>> from sympy import rootof

    >>> [rootof(x**2-3,i) for i in (0,1)]
    [-sqrt(3), sqrt(3)]

    Although ``sqrt`` is printed, there is no ``sqrt`` function so looking for
    ``sqrt`` in an expression will fail:

    >>> from sympy.utilities.misc import func_name
    >>> func_name(sqrt(x))
    'Pow'
    >>> sqrt(x).has(sqrt)
    False

    To find ``sqrt`` look for ``Pow`` with an exponent of ``1/2``:

    >>> (x + 1/sqrt(x)).find(lambda i: i.is_Pow and abs(i.exp) is S.Half)
    {1/sqrt(x)}

    See Also
    ========

    sympy.polys.rootoftools.rootof, root, real_root

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Square_root
    .. [2] https://en.wikipedia.org/wiki/Principal_value
    """
    # arg = sympify(arg) is handled by Pow
    return Pow(arg, S.Half, evaluate=evaluate)


def sqrt(x):
    """
    Compute the square root of x.

    For negative input elements, a complex value is returned
    (unlike `numpy.sqrt` which returns NaN).

    Parameters
    ----------
    x : array_like
       The input value(s).

    Returns
    -------
    out : ndarray or scalar
       The square root of `x`. If `x` was a scalar, so is `out`,
       otherwise an array is returned.

    See Also
    --------
    numpy.sqrt

    Examples
    --------
    For real, non-negative inputs this works just like `numpy.sqrt`:

    >>> import numpy as np

    >>> np.emath.sqrt(1)
    1.0
    >>> np.emath.sqrt([1, 4])
    array([1.,  2.])

    But it automatically handles negative inputs:

    >>> np.emath.sqrt(-1)
    1j
    >>> np.emath.sqrt([-1,4])
    array([0.+1.j, 2.+0.j])

    Different results are expected because:
    floating point 0.0 and -0.0 are distinct.

    For more control, explicitly use complex() as follows:

    >>> np.emath.sqrt(complex(-4.0, 0.0))
    2j
    >>> np.emath.sqrt(complex(-4.0, -0.0))
    -2j
    """
    x = _fix_real_lt_zero(x)
    return nx.sqrt(x)


def sqrt(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SqrtOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def sqrt(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SqrtOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def sqrt(src: _ods_ir.Value, rnd: _Union[_Any, _ods_ir.Attribute], *, ftz: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SqrtOp(src=src, rnd=rnd, ftz=ftz, results=results, loc=loc, ip=ip).result


def sqrt(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SqrtOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def sqrt(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise square root: :math:`\sqrt{x}`.

  This function lowers directly to the `stablehlo.sqrt`_ operation.

  Args:
    x: Input array. Must have floating or complex dtype.
    accuracy: Optional `lax.Tolerance` or `lax.AccuracyMode` object that
      selects the implementation of the op based on the requested accuracy. If
      the implementation cannot satisfy the requested tolerance, the
      compiler will return an error. If mode is specified and there are no
      multiple implementations available, the default implementation will be
      used.

  Returns:
    An array of the same shape and dtype as ``x`` containing the square root.

  See also:
    :func:`jax.lax.pow`: Elementwise power.
    :func:`jax.lax.cbrt`: Elementwise cube root.
    :func:`jax.lax.rsqrt`: Elementwise reciporical square root.

  .. _stablehlo.sqrt: https://openxla.org/stablehlo/spec#sqrt
  """
  return sqrt_p.bind(x, accuracy=accuracy)


def sqrt(x: ArrayLike, /) -> Array:
  """Calculates element-wise non-negative square root of the input array.

  JAX implementation of :obj:`numpy.sqrt`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing the non-negative square root of the elements of ``x``.

  Note:
    - For real-valued negative inputs, ``jnp.sqrt`` produces a ``nan`` output.
    - For complex-valued negative inputs, ``jnp.sqrt`` produces a ``complex`` output.

  See also:
    - :func:`jax.numpy.square`: Calculates the element-wise square of the input.
    - :func:`jax.numpy.power`: Calculates the element-wise base ``x1`` exponential
      of ``x2``.

  Examples:
    >>> x = jnp.array([-8-6j, 1j, 4])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.sqrt(x)
    Array([1.   -3.j   , 0.707+0.707j, 2.   +0.j   ], dtype=complex64)
    >>> jnp.sqrt(-1)
    Array(nan, dtype=float32, weak_type=True)
  """
  out = lax.sqrt(*promote_args_inexact('sqrt', x))
  jnp_error._set_error_if_nan(out)
  return out

