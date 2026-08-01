
def philox_4x32_kernel(key,
                      shape: Shape,
                      unpadded_shape: Shape,
                      block_size: tuple[int, int],
                      offset: typing.ArrayLike = 0,
                      fuse_output: bool = True):
  """Generates random bits using the Philox keyed hash function.

  Args:
    key: A Philox key of shape (2,).
    shape: The shape of the output. Must be divisible by `block_size`.
    unpadded_shape: If `shape` is padded, then this is the shape of the
      output tensor if it were not padded. This is important for indexing
      calculations within the kernel. If `shape` is not padded, then this
      should be equal to `shape`.
    block_size: The block size of the kernel.
    offset: An optional offset to the counts.
    fuse_output: Whether to fuse the output bits into a single value.

  Returns:
    A tensor of random bits of shape `shape` if fuse_output=True. Otherwise,
    this will return a tensor of shape (2, *shape) with the first channel being
    the high bits and the second channel being the low bits.
  """
  shape = tuple(shape)
  if np.prod(shape) > jnp.iinfo(jnp.uint32).max:
    raise ValueError(
        f"Shape too large: {np.prod(shape)} > {np.iinfo(jnp.uint32).max}")

  if (shape[-2] % block_size[-2] != 0) or (shape[-1] % block_size[-1] != 0):
    raise ValueError(
        f"Shape dimension {shape[-2:]} must be divisible by {block_size}")
  grid_dims = shape[:-2] + (
      shape[-2] // block_size[-2], shape[-1] // block_size[1],)
  offset = jnp.array(offset, dtype=jnp.uint32)
  if offset.ndim != 0:
    raise ValueError(f"Offset must be scalar, got {offset.shape}")
  offset = jnp.reshape(offset, (1,))

  def kernel(offset_ref, key_ref, out_ref):
    counts_idx = tuple(pl.program_id(i) for i in range(len(grid_dims)))
    offset = prng_utils.compute_scalar_offset(
        counts_idx, unpadded_shape, block_shape)
    counts_lo = prng_utils.blocked_iota(block_size, unpadded_shape)
    counts_lo = counts_lo + offset.astype(jnp.uint32) + offset_ref[0]
    counts_lo = counts_lo.astype(jnp.uint32)
    # TODO(justinfu): Support hi bits on count.
    _zeros = jnp.zeros_like(counts_lo)
    k1 = jnp.reshape(key_ref[0, 0], (1, 1))
    k2 = jnp.reshape(key_ref[0, 1], (1, 1))
    o1, o2, _, _ = philox_4x32(_zeros, counts_lo, _zeros, _zeros, k1, k2)
    if fuse_output:
      out_bits = o1 ^ o2
      out_ref[...] = out_bits.reshape(out_ref.shape)
    else:
      out_ref[0, ...] = o1.reshape(out_ref[0].shape)
      out_ref[1, ...] = o2.reshape(out_ref[0].shape)

  key = key.reshape((1, 2))
  block_shape = (1,) * (len(shape)-2) + block_size
  if fuse_output:
    out = jax.ShapeDtypeStruct(shape, dtype=jnp.uint32)
    out_spec = pl.BlockSpec(block_shape, lambda *idxs: idxs)
  else:
    out = jax.ShapeDtypeStruct((2,) + shape, dtype=jnp.uint32)
    out_spec = pl.BlockSpec((2,) + block_shape, lambda *idxs: (0, *idxs))
  return pl.pallas_call(
      kernel,
      in_specs=[
          pl.BlockSpec(memory_space=pltpu.SMEM),
          pl.BlockSpec(memory_space=pltpu.SMEM),
      ],
      out_specs=out_spec,
      grid=grid_dims,
      out_shape=out,
  )(offset, key)

