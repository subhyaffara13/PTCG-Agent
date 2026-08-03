from typing import Any

def _aval_to_ref_aval(
    aval: Any,
    meshes: Sequence[pallas_core.Mesh],
) -> state.AbstractRef:
  match aval:
    case state.AbstractRef():
      return aval
    case jax_core.ShapedArray(memory_space=memory_space):
      if memory_space == jax_core.MemorySpace.Device:
        defaults = {mesh.default_memory_space for mesh in meshes}
        if len(defaults) != 1:
          raise ValueError(
              "Multiple meshes with different default memory spaces are not"
              " supported."
          )
        memory_space = list(defaults)[0]
      return state.AbstractRef(aval, memory_space=memory_space)
    case jax_core.AbstractValue():
      return state.AbstractRef(aval, memory_space=None)
    case _ if hasattr(aval, "get_ref_aval"):
      ref_aval = aval.get_ref_aval()
      assert isinstance(ref_aval, state.AbstractRef)
      return ref_aval
    case _:
      raise ValueError(f"Unsupported abstract value type: {type(aval), aval}")

