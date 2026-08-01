
def jit_evict_fn(self):
  self._clear_cache()
  pe.trace_to_jaxpr.evict_weakref(self._fun)
  _infer_params_cached.cache_clear()

