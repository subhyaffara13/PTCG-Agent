
def _earray_shard_arg_handler(xs, shardings, layouts, copy_semantics):
  arrs = [x._data for x in xs]
  phys_shardings = [sharding_impls.physical_sharding(x.aval, sharding)
                    for x, sharding in zip(xs, shardings)]
  # TODO(yashkatariya): `layouts` should be converted to physical layouts.
  return pxla.shard_args(phys_shardings, layouts, copy_semantics, arrs)

