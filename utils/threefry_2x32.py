
def threefry_2x32(keypair, count):
  """Apply the Threefry 2x32 hash.

  Args:
    keypair: a pair of 32bit unsigned integers used for the key.
    count: an array of dtype uint32 used for the counts.

  Returns:
    An array of dtype uint32 with the same shape as `count`.
  """
  key1, key2 = keypair
  if not lax.dtype(key1) == lax.dtype(key2) == lax.dtype(count) == np.uint32:
    msg = "threefry_2x32 requires uint32 arguments, got {}"
    raise TypeError(msg.format([lax.dtype(x) for x in [key1, key2, count]]))

  flat_count = count.ravel()
  odd_size = flat_count.shape[0] % 2
  if core.is_constant_dim(odd_size):
    if odd_size:
      x = list(jnp.split(jnp.concatenate([flat_count, jnp.uint32([0])]), 2))
    else:
      x = list(jnp.split(flat_count, 2))
  else:
    # With symbolic shapes we cannot always tell statically if odd_size is true
    # or false, so we rewrite this without a conditional.
    flat_count_padded = jnp.concatenate([flat_count, jnp.uint32([0])])
    flat_count_padded_half_size = flat_count_padded.shape[0] // 2
    x = [
      lax_slicing.dynamic_slice(flat_count_padded, (0,),
                                (flat_count_padded_half_size,)),
      lax_slicing.dynamic_slice(flat_count_padded,
                                (flat_count_padded_half_size,),
                                (flat_count_padded_half_size,))
    ]
  assert x[0].shape == x[1].shape, (x[0].shape, x[1].shape)

  x = threefry2x32_p.bind(key1, key2, x[0], x[1])
  out = jnp.concatenate(x)
  assert out.dtype == np.uint32
  if core.is_constant_dim(odd_size):
    return lax.reshape(out[:-1] if odd_size else out, count.shape)
  else:
    out_no_padding = lax_slicing.dynamic_slice(out, (0,), (flat_count.shape[0],))
  return lax.reshape(out_no_padding, count.shape)

