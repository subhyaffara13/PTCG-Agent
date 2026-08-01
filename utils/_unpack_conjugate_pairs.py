
def _unpack_conjugate_pairs(w: Array, vr: Array) -> Array:
  # cusolver, like LAPACK, uses a packed representation of the complex
  # eigenvectors, where the (re, im) vectors are adjacent and shared by the
  # conjugate pair:
  # https://docs.nvidia.com/cuda/cusolver/index.html?highlight=geev#cusolverdnxgeev
  if w.size == 0:
    return lax.complex(vr, lax.full_like(vr, 0))

  is_real = ((w.imag == 0) | (w.imag == np.nan))
  # Finds the positions at which each conjugate pair starts, via the parity of
  # the count of the number of complex numbers seen.
  conj_pair_start = control_flow.cumsum((~is_real).astype(int),
                                        axis=len(w.shape) - 1)
  conj_pair_start = conj_pair_start % 2 == 1
  pads = [(0, 0, 0)] * (len(vr.shape))
  pads[-1] = (-1, 1, 0)
  vr_shifted_left = lax.pad(vr, lax._zero(vr), pads)
  pads[-1] = (1, -1, 0)
  vr_shifted_right = lax.pad(vr, lax._zero(vr), pads)
  dims = list(np.delete(np.arange(len(vr.shape), dtype=np.int32), -2))
  is_real = lax.broadcast_in_dim(is_real, vr.shape, broadcast_dimensions=dims)
  conj_pair_start = lax.broadcast_in_dim(conj_pair_start, vr.shape,
                                         broadcast_dimensions=dims)
  re = lax.select(is_real | conj_pair_start, vr, vr_shifted_right)
  im = lax.select(conj_pair_start, vr_shifted_left, -vr)
  im = lax.select(is_real, lax.full_like(vr, 0), im)
  return lax.complex(re, im)

