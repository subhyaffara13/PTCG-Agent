
def canonicalize_sharding_for_samplers(out_sharding, name, shape):
  out_sharding = canonicalize_sharding(out_sharding, name)
  cur_mesh = get_abstract_mesh()
  if cur_mesh.are_all_axes_explicit and out_sharding is None and not shape:
    # when shape is empty i.e. scalar, we can choose a replicated sharding.
    out_sharding = NamedSharding(cur_mesh, P())
  return out_sharding

