
def everything_saveable(*_, **__) -> bool:
  """The default strategy, as if ``jax.checkpoint`` were not being used at all.

  This is the effective policy without any use of jax.remat."""
  return True

