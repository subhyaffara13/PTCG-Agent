
def fft_abstract_eval(x, fft_type, fft_lengths):
  if len(fft_lengths) > x.ndim:
    raise ValueError(f"FFT input shape {x.shape} must have at least as many "
                    f"input dimensions as fft_lengths {fft_lengths}.")
  if fft_type == FftType.RFFT:
    if x.dtype not in (np.float32, np.float64):
      raise ValueError(f"RFFT input must be float32 or float64, got {x.dtype}")
    if x.shape[-len(fft_lengths):] != fft_lengths:
      raise ValueError(f"RFFT input shape {x.shape} minor dimensions must "
                      f"be equal to fft_lengths {fft_lengths}")
    shape = (x.shape[:-len(fft_lengths)] + fft_lengths[:-1]
             + (fft_lengths[-1] // 2 + 1,))
    dtype = _complex_dtype(x.dtype)
  elif fft_type == FftType.IRFFT:
    if not np.issubdtype(x.dtype, np.complexfloating):
      raise ValueError("IRFFT input must be complex64 or complex128, got "
                       f"{x.dtype}")
    if x.shape[-len(fft_lengths):-1] != fft_lengths[:-1]:
      raise ValueError(f"IRFFT input shape {x.shape} minor dimensions must "
                      "be equal to all except the last fft_length, got "
                      f"{fft_lengths=}")
    shape = x.shape[:-len(fft_lengths)] + fft_lengths
    dtype = _real_dtype(x.dtype)
  else:
    if not np.issubdtype(x.dtype, np.complexfloating):
      raise ValueError("FFT input must be complex64 or complex128, got "
                       f"{x.dtype}")
    if x.shape[-len(fft_lengths):] != fft_lengths:
      raise ValueError(f"FFT input shape {x.shape} minor dimensions must "
                      f"be equal to fft_lengths {fft_lengths}")
    shape = x.shape
    dtype = x.dtype
  if x.mat.unreduced or x.mat.reduced:
    raise NotImplementedError
  return x.update(shape=shape, dtype=dtype)

