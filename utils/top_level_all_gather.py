
def top_level_all_gather(xs, out_sharding, *, multi_dim: bool = False):
  if not get_abstract_mesh().are_all_axes_explicit:
    raise ValueError(
        'top_level_all_gather works when all mesh axes of context mesh are'
        f' explicit. Got {get_abstract_mesh()}')
  x_flat, treedef = tree_flatten(xs)
  out_sharding_flat = api_util.flatten_axis_resources(
      "top_level_all_gather out_sharding", treedef, out_sharding,
      tupled_args=True)
  x_avals_flat = [core.typeof(x) for x in x_flat]
  out_flat = [_top_level_ag(x, aval, sh, multi_dim)
              for x, aval, sh in zip(x_flat, x_avals_flat, out_sharding_flat)]
  return tree_unflatten(treedef, out_flat)

