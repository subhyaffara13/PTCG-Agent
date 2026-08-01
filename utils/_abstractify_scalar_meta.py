
def _abstractify_scalar_meta(x):
  raise TypeError(f"JAX scalar type {x} cannot be interpreted as a JAX array.")

