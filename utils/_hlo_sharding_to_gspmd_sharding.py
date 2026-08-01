
def _hlo_sharding_to_gspmd_sharding(
    hlo_sharding: HloSharding | None,
    device_assignment: Sequence[_jax.Device]
    ) -> sharding_impls.GSPMDSharding | None:
  if hlo_sharding is None:
    return None
  return sharding_impls.GSPMDSharding(device_assignment, hlo_sharding)

