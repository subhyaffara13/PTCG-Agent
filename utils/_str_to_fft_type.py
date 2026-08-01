
def _str_to_fft_type(s: str) -> FftType:
  if s in ("fft", "FFT"):
    return FftType.FFT
  elif s in ("ifft", "IFFT"):
    return FftType.IFFT
  elif s in ("rfft", "RFFT"):
    return FftType.RFFT
  elif s in ("irfft", "IRFFT"):
    return FftType.IRFFT
  else:
    raise ValueError(f"Unknown FFT type '{s}'")

