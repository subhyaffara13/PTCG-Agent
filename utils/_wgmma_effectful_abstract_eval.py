
def _wgmma_effectful_abstract_eval(acc, lhs_ref, *args, **kwargs):
  del args, kwargs
  return acc, {
      gpu_core._wgmma_pipeline_effect,
      state.ReadEffect(2),
      *([state.ReadEffect(1)] if isinstance(lhs_ref, state.AbstractRef) else [])
  }

