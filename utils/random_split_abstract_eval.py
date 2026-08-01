
def random_split_abstract_eval(keys_aval, *, shape):
  # TODO(yashkatariya): random_split should take sharding as an arg too so we
  # don't choose None here?
  if keys_aval.sharding.mesh.empty:
    out_sharding = core.get_cur_mesh_sharding()
  else:
    new_spec = (*keys_aval.sharding.spec, *[None] * len(shape))
    out_sharding = keys_aval.sharding.update(spec=new_spec)
  return keys_shaped_array(keys_aval.dtype._impl, (*keys_aval.shape, *shape),
                           out_sharding, keys_aval.mat)

