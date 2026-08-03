import math


def _ref_group_size(refs: _GPUMemoryRefTree) -> int:
  size = 0
  for ref in jax.tree.leaves(refs):
    # Make sure that the start of each ref is aligned with `SMEM_ALIGNMENT`.
    size = align_to(size, SMEM_ALIGNMENT)
    if jnp.issubdtype(ref.dtype, jnp.integer):
      nbits = jnp.iinfo(ref.dtype).bits
    elif jnp.issubdtype(ref.dtype, jnp.floating):
      nbits = jnp.finfo(ref.dtype).bits
    else:
      raise NotImplementedError(f"Unsupported dtype: {ref.dtype}")
    ref_bits = math.prod(ref.shape) * nbits
    if ref_bits % 8:
      raise ValueError(
          "Only byte-aligned shapes are supported. Got shape:"
          f" {ref.dtype}{ref.shape}"
      )
    size += ref_bits // 8
  return size

