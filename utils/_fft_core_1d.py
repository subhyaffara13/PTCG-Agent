
def _fft_core_1d(func_name: str, fft_type: lax_fft.FftType,
                 a: ArrayLike, n: int | None, axis: int | None,
                 norm: str | None) -> Array:
  _axis_check_1d(func_name, axis)
  axes = None if axis is None else [axis]
  s = None if n is None else [n]
  return _fft_core(func_name, fft_type, a, s, axes, norm)

