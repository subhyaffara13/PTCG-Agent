
def _ref_to_lojax(init_val, *, memory_space, kind):
  from jax._src.state.types import AbstractRef  # pyrefly: ignore[missing-import]
  val_ty = typeof(init_val)
  hival_of_refs = val_ty.raise_val(*map(new_ref, val_ty.lower_val(init_val)))
  return Ref(AbstractRef(val_ty), hival_of_refs)

