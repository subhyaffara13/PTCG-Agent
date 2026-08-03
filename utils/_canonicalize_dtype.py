from typing import Any

def _canonicalize_dtype(x64_enabled: bool, allow_extended_dtype: bool, dtype: Any) -> DType | ExtendedDType:
  if issubdtype(dtype, extended):
    if not allow_extended_dtype:
      raise ValueError(f"Internal: canonicalize_dtype called on extended dtype {dtype} "
                       "with allow_extended_dtype=False")
    return dtype
  try:
    dtype_ = np.dtype(dtype)
  except TypeError as e:
    raise TypeError(f'dtype {dtype!r} not understood') from e

  if x64_enabled:
    return dtype_
  else:
    return _dtype_to_32bit_dtype.get(dtype_, dtype_)

