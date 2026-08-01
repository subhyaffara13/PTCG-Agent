
def insert_reduced_reshard(args):
  cur_mesh = mesh_lib.get_abstract_mesh()
  if not cur_mesh.are_all_axes_explicit:
    return args
  # TODO(yashkatariya): Handle >2 args too
  if len(args) != 2:
    return args
  in_reduced = [aval.sharding.spec.reduced
                if isinstance(aval := shaped_abstractify(a), ShapedArray)
                else frozenset() for a in args]
  out_reduced = frozenset.union(*in_reduced)
  out = []
  for arg, src_reduced in zip(args, in_reduced):
    aval = shaped_abstractify(arg)
    if (isinstance(aval, ShapedArray) and aval.ndim == 0 and out_reduced and
        (get_replicated_axes(aval.sharding.spec, cur_mesh) & out_reduced) == out_reduced):
      from jax._src.pjit import reshard  # type: ignore
      out.append(reshard(arg, P(reduced=out_reduced)))
    else:
      out.append(arg)
  return out

