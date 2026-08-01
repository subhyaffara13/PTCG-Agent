
def _maybe_static_check(pred: bool, msg: str):
  # Tries to emit a static error if possible, otherwise falls back to runtime.
  from jax.experimental import checkify

  if isinstance(pred, jax.Array):
    checkify.check(pred, msg, debug=True)
  else:
    if not pred:
      raise ValueError(msg)

