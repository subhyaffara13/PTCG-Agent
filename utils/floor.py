
def floor(x):
    if is_integer_type(x):
        return clone(x)
    fn = ops_wrapper("floor")
    return make_pointwise(fn)(x)


def floor(a):
    return prims.floor(a)


def floor(g: jit_utils.GraphContext, input):
    return g.op("Floor", input)


def floor(x):
    """Evaluates the floor of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.floor(x))
    elif isinstance(x, interval):
        if x.is_valid is False:
            return interval(-np.inf, np.inf, is_valid=False)
        else:
            start = np.floor(x.start)
            end = np.floor(x.end)
            #continuous over the argument
            if start == end:
                return interval(start, end, is_valid=x.is_valid)
            else:
                #not continuous over the interval
                return interval(start, end, is_valid=None)
    else:
        return NotImplementedError


def floor(x: Array, /) -> Array:
    if cp.issubdtype(x.dtype, cp.integer):
        return x.copy()
    return cp.floor(x)


def floor(x: Array, /) -> Array:
    if np.__version__ < '2' and np.issubdtype(x.dtype, np.integer):
        return x.copy()
    return np.floor(x)


def floor(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FloorOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def floor(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return FloorOp(operand=operand, results=results, loc=loc, ip=ip).result


def floor(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return FloorOp(operand=operand, results=results, loc=loc, ip=ip).result


def floor(x: ArrayLike) -> Array:
  r"""Elementwise floor: :math:`\left\lfloor x \right\rfloor`.

  This function lowers directly to the `stablehlo.floor`_ operation.

  Args:
    x: input array. Must have floating-point type.

  Returns:
    Array of same shape and dtype as ``x``, containing values rounded
    to the next integer toward negative infinity.

  See also:
    - :func:`jax.lax.ceil`: round to the next integer toward positive infinity
    - :func:`jax.lax.round`: round to the nearest integer

  .. _stablehlo.floor: https://openxla.org/stablehlo/spec#floor
  """
  return floor_p.bind(x)


def floor(x: ArrayLike, /) -> Array:
  """Round input to the nearest integer downwards.

  JAX implementation of :obj:`numpy.floor`.

  Args:
    x: input array or scalar. Must not have complex dtype.

  Returns:
    An array with same shape and dtype as ``x`` containing the values rounded to
    the nearest integer that is less than or equal to the value itself.

  See also:
    - :func:`jax.numpy.fix`: Rounds the input to the nearest integer towards zero.
    - :func:`jax.numpy.trunc`: Rounds the input to the nearest integer towards
      zero.
    - :func:`jax.numpy.ceil`: Rounds the input up to the nearest integer.

  Examples:
    >>> key = jax.random.key(42)
    >>> x = jax.random.uniform(key, (3, 3), minval=-5, maxval=5)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...     print(x)
    [[-0.11  1.8   1.16]
     [ 0.61 -0.49  0.86]
     [-4.25  2.75  1.99]]
    >>> jnp.floor(x)
    Array([[-1.,  1.,  1.],
           [ 0., -1.,  0.],
           [-5.,  2.,  1.]], dtype=float32)
  """
  x = ensure_arraylike('floor', x)
  if dtypes.isdtype(x.dtype, ('integral', 'bool')):
    return x
  return lax.floor(*promote_args_inexact('floor', x))

