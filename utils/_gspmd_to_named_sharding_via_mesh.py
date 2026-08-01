
def _gspmd_to_named_sharding_via_mesh(
    out_s: GSPMDSharding, mesh: Mesh | AbstractMesh
) -> NamedSharding:
  spec = parse_flatten_op_sharding(out_s._hlo_sharding, mesh)[0]
  return cached_named_sharding(mesh, spec, out_s.memory_kind)

