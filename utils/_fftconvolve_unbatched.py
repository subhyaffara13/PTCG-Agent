
def _fftconvolve_unbatched(in1: Array, in2: Array, mode: str) -> Array:
  full_shape = tuple(s1 + s2 - 1 for s1, s2 in zip(in1.shape, in2.shape))

  # TODO(jakevdp): potentially use next_fast_len to evaluate with a more efficient shape.
  fft_shape = full_shape  # tuple(next_fast_len(s) for s in full_shape)

  if mode == 'valid':
    no_swap = all(s1 >= s2 for s1, s2 in zip(in1.shape, in2.shape))
    swap = all(s1 <= s2 for s1, s2 in zip(in1.shape, in2.shape))
    if not (no_swap or swap):
      raise ValueError("For 'valid' mode, One input must be at least as "
                       "large as the other in every dimension.")
    if swap:
      in1, in2 = in2, in1

  if (all(s1 == 1 or s2 == 1 for s1, s2 in zip(in1.shape, in2.shape))):
    conv = in1 * in2
  else:
    if jnp.iscomplexobj(in1):
      fft, ifft = jnp.fft.fftn, jnp.fft.ifftn
    else:
      fft, ifft = jnp.fft.rfftn, jnp.fft.irfftn
    sp1 = fft(in1, fft_shape)
    sp2 = fft(in2, fft_shape)
    conv = ifft(sp1 * sp2, fft_shape)

  if mode == "full":
    out_shape = full_shape
  elif mode == "same":
    out_shape = in1.shape
  elif mode == "valid":
    out_shape = tuple(s1 - s2 + 1 for s1, s2 in zip(in1.shape, in2.shape))
  else:
    raise ValueError(f"Unrecognized {mode=}")

  start_indices = tuple((full_size - out_size) // 2
                        for full_size, out_size in zip(full_shape, out_shape))
  return lax.dynamic_slice(conv, start_indices, out_shape)

