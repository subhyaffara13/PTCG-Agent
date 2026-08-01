
def _unmatch(mesh, check_vma, in_spec, manual_axes, x):
  if check_vma:
    used_axes = _spec_to_vma(in_spec)
    dst = P(order_wrt_mesh(mesh, used_axes), unreduced=in_spec.unreduced,
            reduced=in_spec.reduced)
  else:
    dst = P(mesh.axis_names)
    check_vma = False
  return shard_map(_add_singleton, mesh=mesh, in_specs=(in_spec,),
                   out_specs=dst, check_vma=check_vma, axis_names=manual_axes)(x)

