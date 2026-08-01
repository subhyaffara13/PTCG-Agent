
def reciprocal(a):
    return prims.reciprocal(a)


def reciprocal(g: jit_utils.GraphContext, self):
    # torch.reciprocal implicitly casts to float, so we do the same.
    if not symbolic_helper._is_fp(self):
        self = g.op("Cast", self, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    return g.op("Reciprocal", self)


def Reciprocal(name, a, b):
    r"""Creates a continuous random variable with a reciprocal distribution.


    Parameters
    ==========

    a : Real number, :math:`0 < a`
    b : Real number, :math:`a < b`

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Reciprocal, density, cdf
    >>> from sympy import symbols
    >>> a, b, x = symbols('a, b, x', positive=True)
    >>> R = Reciprocal('R', a, b)

    >>> density(R)(x)
    1/(x*(-log(a) + log(b)))
    >>> cdf(R)(x)
    Piecewise((log(a)/(log(a) - log(b)) - log(x)/(log(a) - log(b)), a <= x), (0, True))

    Reference
    =========

    .. [1] https://en.wikipedia.org/wiki/Reciprocal_distribution

    """
    return rv(name, ReciprocalDistribution, (a, b))


def reciprocal(input: _ods_ir.Value[_ods_ir.VectorType], *, approx: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, full_range: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ReciprocalOp(input=input, approx=approx, full_range=full_range, results=results, loc=loc, ip=ip).result


def reciprocal(x: ArrayLike) -> Array:
  r"""Elementwise reciprocal: :math:`1 \over x`."""
  return integer_pow(x, -1)


def reciprocal(x: ArrayLike, /) -> Array:
  """Calculate element-wise reciprocal of the input.

  JAX implementation of :obj:`numpy.reciprocal`.

  The reciprocal is calculated by ``1/x``.

  Args:
    x: input array or scalar.

  Returns:
    An array of same shape as ``x`` containing the reciprocal of each element of
    ``x``.

  Note:
    For integer inputs, ``np.reciprocal`` returns rounded integer output, while
    ``jnp.reciprocal`` promotes integer inputs to floating point.

  Examples:
    >>> jnp.reciprocal(2)
    Array(0.5, dtype=float32, weak_type=True)
    >>> jnp.reciprocal(0.)
    Array(inf, dtype=float32, weak_type=True)
    >>> x = jnp.array([1, 5., 4.])
    >>> jnp.reciprocal(x)
    Array([1.  , 0.2 , 0.25], dtype=float32)
  """
  x = ensure_arraylike("reciprocal", x)
  x, = promote_dtypes_inexact(x)
  return lax.integer_pow(x, -1)


def reciprocal(x, *, approx=False, full_range=True):
  """Computes the reciprocal of an array.

  Args:
    x: The array to compute the reciprocal of.
    approx: Whether to use an approximate reciprocal.
    full_range: Whether to use the full range of the input. If False, compilers
      may produce non-IEEE compliant results for edge cases, but may be faster.
      On TPU, setting it to `False` may produce incorrect results when `x` or
      output is ±inf or NaN; or when `x` is ±1/flt_min or ±0.

  Returns:
    The reciprocal of the array.
  """
  return reciprocal_p.bind(x, approx=approx, full_range=full_range)

