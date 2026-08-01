
def _cond_print(condition, message, **kwargs):
  """Prints message if condition is true."""
  jax.lax.cond(
      condition,
      lambda _: jax.debug.print(message, **kwargs, ordered=True),
      lambda _: None,
      None,
  )

