
def base_arr_shape_to_keys_shape(impl, base_arr_shape):
  base_ndim = len(impl.key_shape)
  return base_arr_shape[:-base_ndim]

