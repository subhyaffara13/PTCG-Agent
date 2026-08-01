
def _global_to_local_aval(global_aval, mesh, pspec):
  pspec = sharding_impls.prepare_axis_resources(pspec, "pspec to array_mapping")
  return pxla.mesh_global_to_local(
      mesh, sharding_impls.get_array_mapping(pspec), global_aval)


def _global_to_local_aval(shape, dtype, sharding):
  """Compute local aval from global shape."""
  pspec_prepared = sharding_impls.prepare_axis_resources(sharding.spec, "pspec")
  global_aval = core.ShapedArray(shape, dtype)
  return pxla.mesh_global_to_local(
      sharding.mesh,
      sharding_impls.get_array_mapping(pspec_prepared),
      global_aval,
  )

