
def _attention_fwd(q, k, v, config: TuningConfig, save_residuals: bool):
  del save_residuals

  out, (lse,) = _attention_forward(q, k, v, config, save_residuals=True)
  return out, (q, k, v, out, lse)

