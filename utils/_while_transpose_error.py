
def _while_transpose_error(*_, **kwargs):
  raise ValueError("Reverse-mode differentiation does not work for "
                   "lax.while_loop or lax.fori_loop with dynamic start/stop values. "
                   "Try using lax.scan, or using fori_loop with static start/stop.")

