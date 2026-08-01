
def _fft_core_nd(arr: Array, fft_type: lax_fft.FftType, s: Shape) -> Array:
  # XLA supports N-D transforms up to N=3 so we use XLA's FFT N-D directly.
  if len(s) <= 3:
    return lax_fft.fft(arr, fft_type, tuple(s))

  # For larger N, we repeatedly apply N<=3 transforms until we reach the
  # requested dimension. We special case N=4 to use two 2-D transforms instead
  # of one 3-D and one 1-D, since we typically expect better accelerator
  # performance when N>1.
  n = 2 if len(s) == 4 else 3
  src = tuple(range(arr.ndim - len(s), arr.ndim - n))
  dst = tuple(range(arr.ndim - len(s) + n, arr.ndim))
  if fft_type in {lax_fft.FftType.RFFT, lax_fft.FftType.FFT}:
    arr = lax_fft.fft(arr, fft_type, tuple(s)[-n:])
    arr = jnp.moveaxis(arr, src, dst)
    arr = _fft_core_nd(arr, lax_fft.FftType.FFT, s[:-n])
    arr = jnp.moveaxis(arr, dst, src)
  else:
    arr = jnp.moveaxis(arr, src, dst)
    arr = _fft_core_nd(arr, lax_fft.FftType.IFFT, s[:-n])
    arr = jnp.moveaxis(arr, dst, src)
    arr = lax_fft.fft(arr, fft_type, tuple(s)[-n:])
  return arr

