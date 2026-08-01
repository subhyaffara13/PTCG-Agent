
def _normal(key, shape, dtype) -> Array:
  if dtypes.issubdtype(dtype, np.complexfloating):
    sqrt2 = np.array(np.sqrt(2), dtype)

    key_re, key_im = _split(key)
    real_dtype = np.array(0, dtype).real.dtype
    _re = _normal_real(key_re, shape, real_dtype).astype(dtype)
    _im = _normal_real(key_im, shape, real_dtype).astype(dtype)
    return (_re + 1j * _im) / sqrt2
  else:
    return _normal_real(key, shape, dtype)

