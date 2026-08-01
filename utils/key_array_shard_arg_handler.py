
def key_array_shard_arg_handler(xs: Sequence[PRNGKeyArray], shardings, layouts,
                                copy_semantics):
  arrs = [x._base_array for x in xs]
  phys_shardings = [physical_sharding(x.aval, sharding)
                    for x, sharding in zip(xs, shardings)]
  # TODO(yashkatariya): `layouts` should be converted to physical layouts.
  return pxla.shard_args(phys_shardings, layouts, copy_semantics, arrs)

