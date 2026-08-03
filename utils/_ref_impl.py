from typing import Any

def _ref_impl(init_val, *, memory_space: Any, kind: Any):
  if memory_space is not None:
    raise NotImplementedError(
        "array ref with memory space only works inside of a `jit`.")
  from jax._src.state.types import AbstractRef  # pyrefly: ignore[missing-import]
  from jax._src.lax.lax import _array_copy  # pyrefly: ignore[missing-import]
  aval = AbstractRef(typeof(init_val), kind=kind)
  return Ref(aval, ArrayRefImpl(aval, _array_copy(init_val)))

