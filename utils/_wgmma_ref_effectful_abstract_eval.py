
def _wgmma_ref_effectful_abstract_eval(acc_aval, a_aval, b_aval, *_, **params):
  del b_aval, params
  if not isinstance(acc_aval, gpu_core.WGMMAAbstractAccumulatorRef):
    raise TypeError(f"Expected WGMMAAbstractAccumulatorRef got {acc_aval}")
  return (), {
      gpu_core._wgmma_pipeline_effect,
      state.WriteEffect(0),
      state.ReadEffect(0),
      state.ReadEffect(2),
      *([state.ReadEffect(1)] if isinstance(a_aval, state.AbstractRef) else [])
  }

