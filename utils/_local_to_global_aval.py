
def _local_to_global_aval(local_aval, mesh, pspec):
  pspec = sharding_impls.prepare_axis_resources(pspec, "pspec to array_mapping")
  return pxla.mesh_local_to_global(
      mesh, sharding_impls.get_array_mapping(pspec), local_aval)


def _local_to_global_aval(shape, dtype, sharding):
  """Compute global aval from local shape."""
  pspec_prepared = sharding_impls.prepare_axis_resources(sharding.spec, "pspec")
  local_aval = core.ShapedArray(shape, dtype)
  return pxla.mesh_local_to_global(
      sharding.mesh,
      sharding_impls.get_array_mapping(pspec_prepared),
      local_aval,
  )

