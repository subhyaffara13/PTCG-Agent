
def _prim_applier(prim, check_vma, params_tup, concrete_mesh, manual_axes,
                  in_specs, out_specs, *args):
  def apply(*args):
    outs = prim.bind(*map(_rem_singleton, args), **dict(params_tup))
    return tree_map(_add_singleton, outs)
  out_specs = list(out_specs) if type(out_specs) is tuple else out_specs
  return shard_map(apply, mesh=concrete_mesh, in_specs=in_specs,
                   out_specs=out_specs, check_vma=check_vma,
                   axis_names=manual_axes)(*args)

