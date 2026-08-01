
def typematch(t1: AbstractValue, t2: AbstractValue,
              no_dtype_check: bool = False) -> bool:
  """Determine whether `t1` and `t2` are equivalent. Ignores weak_type."""
  t1 = t1.normalize()
  t2 = t2.normalize()
  from jax._src.state.types import AbstractRef  # pyrefly: ignore[missing-import]
  if t1 == t2:
    return True
  elif isinstance(t1, ShapedArray) and isinstance(t2, ShapedArray):
    if no_dtype_check:
      return cmp_shape_shd_mat_memsp(t1, t2)
    return t1.dtype == t2.dtype and cmp_shape_shd_mat_memsp(t1, t2)
  elif isinstance(t1, AbstractRef) and isinstance(t2, AbstractRef):
    # We want to use the regular typecheck for ShapedArray here.
    return (typematch(t1.inner_aval, t2.inner_aval, no_dtype_check) and
            (t1.memory_space is None or t2.memory_space is None or
             t1.memory_space == t2.memory_space))
  else:
    return False

