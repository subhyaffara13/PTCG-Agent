
def _fft_impl(x, fft_type, fft_lengths):
  return dispatch.apply_primitive(fft_p, x, fft_type=fft_type, fft_lengths=fft_lengths)

