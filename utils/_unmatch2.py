
def _unmatch2(mesh, prev_manual, spec, x):
  src = P(order_wrt_mesh(mesh, prev_manual), *spec)
  newly_manual = _spec_to_vma(spec)
  dst = P(order_wrt_mesh(mesh, prev_manual | newly_manual))
  return shard_map(lambda x: x, in_specs=src, out_specs=dst,
                   axis_names=prev_manual | newly_manual)(x)

