
def bessel_i0e_impl(x: Array) -> Array:
  if x.dtype == np.float64:
    return _i0e_impl64(x)
  elif x.dtype == np.float32:
    return _i0e_impl32(x)
  else:
    # Have to upcast f16 because the magic Cephes coefficients don't have enough
    # precision for it.
    x_dtype = x.dtype
    x = x.astype(np.float32)
    return convert_element_type(_i0e_impl32(x), x_dtype)

