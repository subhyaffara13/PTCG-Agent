
def _unmap_ref(size, axis, explicit_mesh_axis, ref_aval):
  return AbstractRef(core.unmapped_aval(
      size, axis, ref_aval.inner_aval, explicit_mesh_axis),
                     ref_aval.memory_space, ref_aval.kind)

