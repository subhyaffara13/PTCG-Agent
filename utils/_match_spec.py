
def _match_spec(mesh: Mesh, check_vma, manual_axes, x: JaxType,
                src_pspec: PartitionSpec, dst_pspec: PartitionSpec) -> JaxType:
  fn = HashablePartial(_match, mesh, check_vma, manual_axes, src_pspec,
                       dst_pspec)
  with core.eval_context(), api.disable_jit(False):
    if set(mesh.axis_names) == manual_axes:
      return api.jit(fn, out_shardings=NamedSharding(mesh, dst_pspec))(x)
    return api.jit(fn)(x)

