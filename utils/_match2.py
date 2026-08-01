
def _match2(mesh, prev_manual, spec, x):
  newly_manual = _spec_to_vma(spec)
  src = P(order_wrt_mesh(mesh, prev_manual | newly_manual))
  dst = P(order_wrt_mesh(mesh, prev_manual), *spec)
  return shard_map(lambda x: x, in_specs=src, out_specs=dst,
                   axis_names=prev_manual | newly_manual)(x)

