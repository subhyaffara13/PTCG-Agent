
def check_special_array(name: str, arr: array.ArrayImpl) -> array.ArrayImpl:
  if needs_check_special():
    if dtypes.issubdtype(arr.dtype, np.inexact):
      for buf in arr._arrays:
        _check_special(name, buf.dtype, buf)
  return arr

