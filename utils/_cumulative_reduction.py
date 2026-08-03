from typing import Callable

def _cumulative_reduction(
    name: str, reduction: Callable[..., Array],
    a: ArrayLike, axis: int | None, dtype: DTypeLike | None, out: None = None,
    fill_nan: bool = False, fill_value: ArrayLike = 0,
    promote_integers: bool = False) -> Array:
  """Helper function for implementing cumulative reductions."""
  a = ensure_arraylike(name, a)
  if out is not None:
    raise NotImplementedError(f"The 'out' argument to jnp.{name} is not supported")

  if axis is None or _isscalar(a):
    if not builtins.all(s is None for s in core.typeof(a).sharding.spec):
      raise core.ShardingTypeError(
          "The input should be fully replicated when axis is not specified to"
          f" {name}. Got input type={core.typeof(a)}")
    a = lax.reshape(a, (np.size(a),))
  if axis is None:
    axis = 0

  a_shape = list(np.shape(a))
  num_dims = len(a_shape)
  axis = canonicalize_axis(axis, num_dims)

  if fill_nan:
    a = _where(lax._isnan(a), lax._const(a, fill_value), a)

  computation_type: DType
  result_type: DType
  if dtype is None:
    if promote_integers or a.dtype == np.bool_:
      result_type = _promote_integer_dtype(a.dtype)
    else:
      result_type = a.dtype
    computation_type = result_type
  elif dtype == np.dtype('bool'):
    # Explicit boolean output requires special handling
    # - lax only supports numerical accumulation, so we can't work in bool directly.
    # - we cannot use the original values of a, otherwise e.g. [-1, 1] may cancel.
    result_type = np.dtype(dtype)
    if a.dtype != result_type:
      a = (a != 0)
    computation_type = _promote_integer_dtype(result_type)
  else:
    result_type = dtypes.check_and_canonicalize_user_dtype(dtype, name)
    computation_type = result_type

  a = lax.convert_element_type(a, computation_type)
  result = reduction(a, axis)
  return lax.convert_element_type(result, result_type)

