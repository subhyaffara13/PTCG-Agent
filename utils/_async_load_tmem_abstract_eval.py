
def _async_load_tmem_abstract_eval(src, *avals_flat, tree):
  if src.memory_space != gpu_core.MemorySpace.TMEM:
    raise ValueError("Async load only supports TMEM refs")
  return state_primitives._get_abstract_eval(src, *avals_flat, tree=tree)

