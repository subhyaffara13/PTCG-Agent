
def _make_array_shape(aval: core.ShapedArray) -> xc.Shape:
  aval = core.physical_aval(aval)
  dtype = np.dtype('bool') if aval.dtype == dtypes.float0 else aval.dtype
  return xc.Shape.array_shape(dtype, aval.shape)

