
def default_nary_reduced_rule(*avals, **params):
  cur_mesh = get_abstract_mesh()
  reduced_spec = {r for a in avals if (r := core.getr(a))}
  if len(reduced_spec) > 1:
    raise core.ShardingTypeError(
        'All inputs should be reduced across the same mesh axes. Got specs:'
        f' {reduced_spec}')
  reduced_s, = reduced_spec if reduced_spec else (frozenset(),)
  if reduced_s:
    for a in avals:
      if replicated_axes(a, cur_mesh) & reduced_s:
        raise core.ShardingTypeError(
            'Inputs cannot be replicated on the same axes that another input'
            f' is reduced on. Got input type: {a} and reduced spec: {reduced_s}')
      if (frozenset(flatten_spec(a.sharding.spec)) | a.mat.varying) & reduced_s:
        raise core.ShardingTypeError(
            'Inputs cannot be sharded/varying on the same axes that another'
            ' input is reduced on. Reshard the input which is reduced to be'
            ' sharded on the mesh axes it is reduced on via'
            f' `jax.sharding.reshard(inp, jax.P(...))`. Got input type: {a} and'
            f' reduced spec: {reduced_s}')
  return reduced_s

