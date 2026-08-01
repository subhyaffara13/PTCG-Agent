
def _fft_transpose_rule(t, operand, fft_type, fft_lengths):
  if fft_type == FftType.RFFT:
    result = _rfft_transpose(t, fft_lengths)
  elif fft_type == FftType.IRFFT:
    result = _irfft_transpose(t, fft_lengths)
  else:
    result = fft(t, fft_type, fft_lengths)
  return result,

