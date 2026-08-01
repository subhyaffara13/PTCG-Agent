
def _empty_ref_to_lojax(*, ty, memory_space):
  from jax._src.state.types import AbstractRef  # pyrefly: ignore[missing-import]
  hival_of_refs = ty.raise_val(
      *map(empty_ref, ty.lo_ty(), [memory_space] * len(ty.lo_ty())))
  return Ref(AbstractRef(ty), hival_of_refs)

