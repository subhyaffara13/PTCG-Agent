
def random_bits_abstract_eval(keys_aval, *, bit_width, shape):
  out_shape = (*keys_aval.shape, *shape)
  out_dtype = dtypes.dtype(f'uint{bit_width}')
  # TODO(yashkatariya): random_bits should take an out_sharding argument.
  if keys_aval.sharding.mesh.empty:
    out_sharding = core.get_cur_mesh_sharding()
  else:
    new_spec = (*keys_aval.sharding.spec, *[None] * len(shape))
    out_sharding = keys_aval.sharding.update(spec=new_spec)
  return core.ShapedArray(out_shape, out_dtype, sharding=out_sharding,
                          manual_axis_type=keys_aval.mat)

