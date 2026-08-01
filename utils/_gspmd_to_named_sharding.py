
def _gspmd_to_named_sharding(
    out_s: GSPMDSharding, out_aval, orig_in_s: NamedSharding) -> NamedSharding:
  assert isinstance(out_s, GSPMDSharding)
  assert isinstance(orig_in_s, NamedSharding)
  assert isinstance(orig_in_s.mesh, Mesh)
  if (out_aval is not None and not out_aval.sharding.mesh.empty and
      not out_aval.sharding.mesh._any_axis_manual):
    mesh = _abstract_to_concrete_mesh(
        out_aval.sharding.mesh, out_s._device_assignment)
  else:
    mesh = orig_in_s.mesh
  return sharding_impls._gspmd_to_named_sharding_via_mesh(out_s, mesh)

