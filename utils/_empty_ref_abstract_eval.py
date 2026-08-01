
def _empty_ref_abstract_eval(*, ty, memory_space):
  from jax._src.state.types import AbstractRef  # pyrefly: ignore[missing-import]
  return (AbstractRef(ty, memory_space=memory_space),
          {internal_mutable_array_effect})

