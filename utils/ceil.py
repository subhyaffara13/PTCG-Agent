
def ceil(x):
    if is_integer_type(x):
        return clone(x)
    fn = ops_wrapper("ceil")
    return make_pointwise(fn)(x)


def ceil(a):
    return prims.ceil(a)


def ceil(g: jit_utils.GraphContext, input):
    return g.op("Ceil", input)


def ceil(x):
    """Evaluates the ceiling of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.ceil(x))
    elif isinstance(x, interval):
        if x.is_valid is False:
            return interval(-np.inf, np.inf, is_valid=False)
        else:
            start = np.ceil(x.start)
            end = np.ceil(x.end)
            #Continuous over the interval
            if start == end:
                return interval(start, end, is_valid=x.is_valid)
            else:
                #Not continuous over the interval
                return interval(start, end, is_valid=None)
    else:
        return NotImplementedError


def ceil(x: Array, /) -> Array:
    if cp.issubdtype(x.dtype, cp.integer):
        return x.copy()
    return cp.ceil(x)


def ceil(x: Array, /) -> Array:
    if np.__version__ < '2' and np.issubdtype(x.dtype, np.integer):
        return x.copy()
    return np.ceil(x)


def ceil(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CeilOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def ceil(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CeilOp(operand=operand, results=results, loc=loc, ip=ip).result


def ceil(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CeilOp(operand=operand, results=results, loc=loc, ip=ip).result


def ceil(x: ArrayLike) -> Array:
  r"""Elementwise ceiling: :math:`\left\lceil x \right\rceil`.

  This function lowers directly to the `stablehlo.ceil`_ operation.

  Args:
    x: input array. Must have floating-point type.

  Returns:
    Array of same shape and dtype as ``x``, containing values rounded
    to the next integer toward positive infinity.

  See also:
    - :func:`jax.lax.floor`: round to the next integer toward negative infinity
    - :func:`jax.lax.round`: round to the nearest integer

  .. _stablehlo.ceil: https://openxla.org/stablehlo/spec#ceil
  """
  return ceil_p.bind(x)


def ceil(x: ArrayLike, /) -> Array:
  """Round input to the nearest integer upwards.

  JAX implementation of :obj:`numpy.ceil`.

  Args:
    x: input array or scalar. Must not have complex dtype.

  Returns:
    An array with same shape and dtype as ``x`` containing the values rounded to
    the nearest integer that is greater than or equal to the value itself.

  See also:
    - :func:`jax.numpy.fix`: Rounds the input to the nearest integer towards zero.
    - :func:`jax.numpy.trunc`: Rounds the input to the nearest integer towards
      zero.
    - :func:`jax.numpy.floor`: Rounds the input down to the nearest integer.

  Examples:
    >>> key = jax.random.key(1)
    >>> x = jax.random.uniform(key, (3, 3), minval=-5, maxval=5)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(x)
    [[-0.61  0.34 -0.54]
     [-0.62  3.97  0.59]
     [ 4.84  3.42 -1.14]]
    >>> jnp.ceil(x)
    Array([[-0.,  1., -0.],
           [-0.,  4.,  1.],
           [ 5.,  4., -1.]], dtype=float32)
  """
  x = ensure_arraylike('ceil', x)
  if dtypes.isdtype(x.dtype, ('integral', 'bool')):
    return lax.asarray(x)
  return lax.ceil(*promote_args_inexact('ceil', x))

