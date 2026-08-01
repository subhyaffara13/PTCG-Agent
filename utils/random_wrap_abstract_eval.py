
def random_wrap_abstract_eval(base_arr_aval, *, impl):
  shape = base_arr_shape_to_keys_shape(impl, base_arr_aval.shape)
  sharding = logical_sharding(shape, KeyTy(impl), base_arr_aval.sharding)
  return keys_shaped_array(impl, shape, sharding, base_arr_aval.mat)

