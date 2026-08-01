
def unknown_signature(eqn):
  def is_key(var: core.Atom):
    return hasattr(var.aval, "dtype") and jax.dtypes.issubdtype(var.aval.dtype, jax.dtypes.prng_key)
  return KeyReuseSignature(
    *(Sink(idx) for idx, var in enumerate(eqn.invars) if is_key(var))
  )

