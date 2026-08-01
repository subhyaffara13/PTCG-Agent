
def _pack_elementwise_abstract_eval(*xs, packed_dtype):
  if not xs:
    raise ValueError("At least one source is required")
  first = xs[0]
  if not all(x.shape == first.shape for x in xs):
    raise ValueError("All sources must have the same shape")
  if not all(x.dtype == first.dtype for x in xs):
    raise ValueError("All sources must have the same dtype")
  if not (first.dtype == jnp.float32 and packed_dtype == jnp.bfloat16) and not (
      jnp.issubdtype(first.dtype, jnp.integer)
      and jnp.issubdtype(packed_dtype, jnp.integer)
  ):
    raise ValueError(
        "Only f32 -> bf16 and int -> int are supported. Got"
        f" {first.dtype} and {packed_dtype}"
    )
  packing_factor = _get_elementwise_packing_factor(first.dtype, packed_dtype)
  if len(xs) != packing_factor:
    raise ValueError(
        "The number of sources must match the packing factor "
        f"({packing_factor}), got {len(xs)}"
    )
  out_dtype = jnp.dtype(f"uint{dtypes.itemsize_bits(first.dtype)}")
  return jax_core.ShapedArray(first.shape, out_dtype)

