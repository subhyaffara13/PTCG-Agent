from typing import Any

def lattice_result_type(*args: Any) -> tuple[DType, bool]:
  dtypes, weak_types = zip(*(_dtype_and_weaktype(arg) for arg in args))
  if len(dtypes) == 1:
    out_dtype = dtypes[0]
    out_weak_type = weak_types[0]
  elif len(set(dtypes)) == 1 and not all(weak_types):
    # Trivial promotion case. This allows extended dtypes through.
    out_dtype = dtypes[0]
    out_weak_type = False
  elif all(weak_types) and config.numpy_dtype_promotion.value != config.NumpyDtypePromotion.STRICT:
    # If all inputs are weakly typed, we compute the bound of the strongly-typed
    # counterparts and apply the weak type at the end. This avoids returning the
    # incorrect result with non-canonical weak types (e.g. weak int16).
    # TODO(jakevdp): explore removing this special case.
    result_type = _least_upper_bound(
        config.numpy_dtype_promotion.value, config.enable_x64.value,
        *{_jax_type(dtype, False) for dtype in dtypes})
    out_dtype = dtype(result_type)
    out_weak_type = True
  else:
    result_type = _least_upper_bound(
        config.numpy_dtype_promotion.value, config.enable_x64.value,
        *{_jax_type(d, w) for d, w in zip(dtypes, weak_types)})
    out_dtype = dtype(result_type)
    out_weak_type = any(result_type is t for t in _weak_types)
  return out_dtype, (out_dtype != bool_) and out_weak_type

