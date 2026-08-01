
def _async_store_tmem_abstract_eval(ref, val, *avals_flat, tree):
  if ref.memory_space != gpu_core.MemorySpace.TMEM:
    raise ValueError("Async store only supports TMEM refs")
  _, effects = state_primitives._swap_abstract_eval(
      ref, val, *avals_flat, tree=tree
  )
  return (), effects

