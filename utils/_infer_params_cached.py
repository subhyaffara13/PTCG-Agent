from typing import Callable

def _infer_params_cached(
    fun: Callable, jit_info: PjitInfo, signature: jax_jit.ArgumentSignature,
    in_avals: tuple[core.AbstractValue, ...], ctx_mesh: mesh_lib.Mesh
    ) -> InferParamsCacheEntry:
  return InferParamsCacheEntry()

