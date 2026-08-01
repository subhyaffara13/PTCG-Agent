
def _dot_general_dtype_rule(lhs, rhs, *, dimension_numbers, precision,
                            preferred_element_type: DTypeLike | None,
                            out_sharding, name: str = 'lax.dot_general'):
  if out_sharding is not None and not isinstance(out_sharding, NamedSharding):
    raise NotImplementedError
  del dimension_numbers  # unused
  # We're mostly matching XLA's logic here, namely in shape_inference.cc and
  # primitive_util.h's HigherPrecisionType, e.g.
  # https://github.com/openxla/xla/blob/ea3a841768d0dcf192e5820c9b25c34c73f2226a/xla/primitive_util.h#L329
  def type_properties(dt):
    c = _real_dtype(dt) if dtypes.issubdtype(dt, np.complexfloating) else dt
    return (dtypes.issubdtype(dt, np.complexfloating),
            dtypes.finfo(c).maxexp if dtypes.issubdtype(c, np.floating) else -1,
            dtypes.finfo(c).nmant  if dtypes.issubdtype(c, np.floating) else -1,
            _bit_width(c),
            not dtypes.issubdtype(c, np.unsignedinteger))
  lhs_prop, rhs_prop = type_properties(lhs.dtype), type_properties(rhs.dtype)
  if lhs_prop > rhs_prop:
    result_dtype = lhs.dtype
  elif rhs_prop > lhs_prop:
    result_dtype = rhs.dtype
  else:
    if lhs.dtype != rhs.dtype:
      raise TypeError(f'{name} argument type error: {lhs.dtype}, {rhs.dtype}')
    result_dtype = lhs.dtype
  has_algorithm = isinstance(precision, (DotAlgorithm, DotAlgorithmPreset))
  return _maybe_upcast(result_dtype, preferred_element_type,
                       check_bit_width=not has_algorithm)

