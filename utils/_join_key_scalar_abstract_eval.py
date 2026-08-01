
def _join_key_scalar_abstract_eval(*seeds, impl):
  if len(impl.key_shape) != 2 or impl.key_shape[0] != 1:
    raise ValueError(f"Key shape must be (1, N), got {impl.key_shape}")
  if len(seeds) != impl.key_shape[1]:
    raise ValueError(
        f"Number of seeds must match key shape, got {len(seeds)}"
        f" != {impl.key_shape[1]}."
    )
  return jax_core.ShapedArray((), dtype=jax_prng.KeyTy(impl))

