
def nothing_saveable(*_, **__) -> bool:
  """Rematerialize everything, as if a custom policy were not being used at all.

  This is the effective policy when using jax.remat without explicit policy."""
  return False

