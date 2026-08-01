
def trunc(x):
    if is_integer_type(x):
        return clone(x)
    fn = ops_wrapper("trunc")
    return make_pointwise(fn)(x)


def trunc(a):
    return prims.trunc(a)


def trunc(f, p, *gens, **args):
    """
    Reduce ``f`` modulo a constant ``p``.

    Examples
    ========

    >>> from sympy import trunc
    >>> from sympy.abc import x

    >>> trunc(2*x**3 + 3*x**2 + 5*x + 7, 3)
    -x**3 - x + 1

    """
    options.allowed_flags(args, ['auto', 'polys'])

    try:
        F, opt = poly_from_expr(f, *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('trunc', 1, exc)

    result = F.trunc(sympify(p))

    if not opt.polys:
        return result.as_expr()
    else:
        return result


def trunc(x: Array, /) -> Array:
    if cp.issubdtype(x.dtype, cp.integer):
        return x.copy()
    return cp.trunc(x)


def trunc(x: Array, /) -> Array:
    if np.__version__ < '2' and np.issubdtype(x.dtype, np.integer):
        return x.copy()
    return np.trunc(x)


def trunc(res: _ods_ir.Type, arg: _ods_ir.Value, overflow_flags, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TruncOp(res=res, arg=arg, overflowFlags=overflow_flags, loc=loc, ip=ip).result


def trunc(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TruncOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def trunc(x: ArrayLike) -> Array:
  """Round input to the nearest integer towards zero.

  JAX implementation of :func:`numpy.trunc`.

  Args:
    x: input array or scalar.

  Returns:
    An array with same shape and dtype as ``x`` containing the rounded values.

  See also:
    - :func:`jax.numpy.fix`: Rounds the input to the nearest integer towards zero.
    - :func:`jax.numpy.ceil`: Rounds the input up to the nearest integer.
    - :func:`jax.numpy.floor`: Rounds the input down to the nearest integer.

  Examples:
    >>> key = jax.random.key(42)
    >>> x = jax.random.uniform(key, (3, 3), minval=-10, maxval=10)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(x)
    [[-0.23  3.6   2.33]
     [ 1.22 -0.99  1.72]
     [-8.5   5.5   3.98]]
    >>> jnp.trunc(x)
    Array([[-0.,  3.,  2.],
           [ 1., -0.,  1.],
           [-8.,  5.,  3.]], dtype=float32)
  """
  x = util.ensure_arraylike('trunc', x)
  if dtypes.isdtype(x.dtype, ('integral', 'bool')):
    return x
  return where(lax.lt(x, lax._const(x, 0)), ufuncs.ceil(x), ufuncs.floor(x))

