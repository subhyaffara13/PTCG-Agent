
def _get_monoid_reducer(monoid_op: Callable,
                        xs: Sequence[Array]) -> Callable | None:
  if len(xs) != 1:
    return None
  x, = xs
  aval = core.typeof(x)
  dtype = _dtype(x)
  if core.is_concrete(x) and aval.shape == ():
    val = core.to_concrete_value(x)
    # allow bitwise reductions for boolean and integer types
    _is_intlike = dtype == np.bool_ or dtypes.issubdtype(dtype, np.integer)
    if monoid_op is add:
      return reduce_sum if np.equal(val, 0) else None
    elif monoid_op is mul:
      return reduce_prod if np.equal(val, 1) else None
    elif monoid_op is bitwise_or and _is_intlike:
      return reduce_or if np.equal(val, _get_bitwise_or_identity(dtype)) else None
    elif monoid_op is bitwise_and and _is_intlike:
      return reduce_and if np.equal(val, _get_bitwise_and_identity(dtype)) else None
    elif monoid_op is bitwise_xor and _is_intlike:
      return reduce_xor if np.equal(val, _get_bitwise_or_identity(dtype)) else None
    elif monoid_op is max:
      return reduce_max if np.equal(val, _get_max_identity(dtype)) else None
    elif monoid_op is min:
      return reduce_min if np.equal(val, _get_min_identity(dtype)) else None
  return None

