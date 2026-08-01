
def _temporary_dtype_exception(a, a_) -> bool:
  if isinstance(a, core.ShapedArray) and isinstance(a_, core.ShapedArray):
    return a.shape == a_.shape and a_.dtype == float0
  return False


def _temporary_dtype_exception(a, a_) -> bool:
  if isinstance(a, core.ShapedArray) and isinstance(a_, core.ShapedArray):
    return (a.shape == a_.shape and
            core.typematch(a, a_, no_dtype_check=True) and
            (dtypes.issubdtype(a_.dtype, dtypes.extended) or
             dtypes.issubdtype(a.dtype, dtypes.np.inexact)))
  return False

