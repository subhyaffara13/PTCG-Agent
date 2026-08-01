
def threefry_2x32_count(key,
                 shape: Shape,
                 unpadded_shape: Shape,
                 block_size: tuple[int, int]):
  """Generates random bits using the Threefry hash function.

  This function is a fusion of prng.shaped_iota and prng.threefry_2x32 from
  the JAX core library.

  Args:
    key: A threefry key of shape (2,).
    shape: The shape of the output. Must be divisible by `block_size`.
    unpadded_shape: If `shape` is padded, then this is the shape of the
      output tensor if it were not padded. This is important for indexing
      calculations within the kernel. If `shape` is not padded, then this
      should be equal to `shape`.
    block_size: The block size of the kernel.

  Returns:
    A tensor of random bits of shape `shape`.
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

  def kernel(key_ref, out_ref):
    counts_idx = tuple(pl.program_id(i) for i in range(len(grid_dims)))
    offset = prng_utils.compute_scalar_offset(
        counts_idx, unpadded_shape, block_shape)
    counts_lo = prng_utils.blocked_iota(block_size, unpadded_shape)
    counts_lo = counts_lo + offset.astype(jnp.uint32)
    counts_lo = counts_lo.astype(jnp.uint32)
    # TODO(justinfu): Support hi bits on count.
    counts_hi = jnp.zeros_like(counts_lo)
    k1 = jnp.reshape(key_ref[0, 0], (1, 1))
    k2 = jnp.reshape(key_ref[0, 1], (1, 1))
    o1, o2 = threefry2x32.threefry2x32_p.bind(
        k1, k2, counts_hi, counts_lo)
    out_bits = o1 ^ o2
    out_ref[...] = out_bits.reshape(out_ref.shape)

  key = key.reshape((1, 2))
  out = jax.ShapeDtypeStruct(shape, dtype=jnp.uint32)
  block_shape = (1,) * (len(shape)-2) + block_size
  result = pl.pallas_call(
      kernel,
      in_specs=[pl.BlockSpec(memory_space=pltpu.SMEM)],
      out_specs=pl.BlockSpec(block_shape, lambda *idxs: idxs),
      grid=grid_dims,
      out_shape=out,
  )(key)
  return result

