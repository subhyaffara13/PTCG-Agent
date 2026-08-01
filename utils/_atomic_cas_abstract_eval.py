
def _atomic_cas_abstract_eval(ref_aval, cmp_aval, val_aval):
  if cmp_aval.dtype != val_aval.dtype or cmp_aval.shape != val_aval.shape:
    raise ValueError("cmp and val must have identical dtypes and shapes")
  if ref_aval.shape:
    raise ValueError("ref must be scalar.")
  if cmp_aval.shape:
    raise ValueError("cmp must be scalar.")
  if val_aval.shape:
    raise ValueError("val must be scalar.")
  return jax_core.ShapedArray(val_aval.shape, val_aval.dtype), {
      state.WriteEffect(0)
  }

