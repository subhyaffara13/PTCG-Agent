import math


def _rfft_transpose(t, fft_lengths):
  # The transpose can be computed directly using irfft with a mask to account
  # for Hermitian redundancy. Mask values are 1 for DC and Nyquist, 2 for others.
  n = fft_lengths[-1]
  is_odd = n % 2
  m = t.shape[-1]
  mask = lax.full_like(t, 2.0, shape=(m,))
  mask = slicing.dynamic_update_slice(
      mask, lax.full_like(t, 1.0, shape=(1,)), (0,)
  )
  if not is_odd:
    mask = slicing.dynamic_update_slice(
        mask, lax.full_like(t, 1.0, shape=(1,)), (m - 1,)
    )

  N = math.prod(fft_lengths)
  # The mask is along the last dimension.
  mask = lax.expand_dims(mask, range(t.ndim - 1))
  out = N * fft(lax.conj(t) / mask, FftType.IRFFT, fft_lengths)
  assert out.dtype == _real_dtype(t.dtype), (out.dtype, t.dtype)
  return out

