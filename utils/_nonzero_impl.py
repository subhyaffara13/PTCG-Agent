
def _nonzero_impl(a: ArrayLike, *, size: int, axes: tuple[int, ...], out_dtype: np.dtype) -> tuple[Array, ...]:
  """Main implementation of nonzero primitive."""
  a = jnp.asarray(a)
  out_dtype = dtypes._maybe_canonicalize_explicit_dtype(out_dtype, "nonzero")
  axes = tuple(sorted(axes))

  if not axes:
    return ()

  batch_axes = [ax for ax in range(a.ndim) if ax not in axes]
  if a.size == 0 or size == 0:
    return tuple(jnp.empty((*batch_axes, size), dtype=out_dtype)
                 for _ in axes)

  transposed_a = jnp.transpose(a, (*batch_axes, *axes))

  batch_shape = transposed_a.shape[:len(batch_axes)]
  sub_shape = transposed_a.shape[len(batch_axes):]
  strides = np.cumprod(sub_shape[::-1])[::-1] // sub_shape
  strides = tuple(strides.tolist())

  flattened_a = transposed_a.reshape(*batch_shape, -1)
  mask = flattened_a if flattened_a.dtype == bool else (flattened_a != 0)
  cs_mask = jnp.cumsum(mask, axis=-1)

  bincount = jnp.zeros((*batch_shape, size), dtype=cs_mask.dtype)
  mesh_dims = jnp.ogrid[tuple(slice(None, sz) for sz in batch_shape)]
  mesh_dims = [lax.expand_dims(m, [m.ndim]) for m in mesh_dims]
  bincount = bincount.at[(*mesh_dims, cs_mask)].add(1, mode='drop')
  flat_indices = jnp.cumsum(bincount, axis=-1)

  out = [(flat_indices // stride) % sz for stride, sz in zip(strides, sub_shape)]
  counts = mask.sum(axis=-1, keepdims=True)
  fill_mask = lax.expand_dims(jnp.arange(size), range(counts.ndim - 1)) >= counts
  return tuple(lax.convert_element_type(jnp.where(fill_mask, 0, entry), out_dtype) for entry in out)

