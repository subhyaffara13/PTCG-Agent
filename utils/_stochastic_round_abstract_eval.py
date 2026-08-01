
def _stochastic_round_abstract_eval(x, random_bits, *, target_dtype):
  if random_bits.shape != x.shape:
    raise ValueError(
        "The shape of `random_bits` must match the shape of `x` for "
        f"stochastic_round, but got {random_bits.shape} and {x.shape}"
    )
  if random_bits.dtype != jnp.dtype("uint32"):
    raise ValueError(
        "The dtype of `random_bits` must be uint32 for stochastic_round, "
        f"but got {random_bits.dtype}"
    )
  return jax_core.ShapedArray(x.shape, target_dtype)

