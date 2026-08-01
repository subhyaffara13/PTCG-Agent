
def _module_to_bytecode(module: ir.Module) -> bytes:
  # `target_version` is used to manage situations when a StableHLO producer
  # and a StableHLO consumer were built using different versions of StableHLO.
  #
  # Each StableHLO version `producer_version` has a compatibility window,
  # i.e. range of versions [`consumer_version_min`, `consumer_version_max`],
  # where StableHLO portable artifacts serialized by `producer_version`
  # can be deserialized by `consumer_version` within the window.
  # See https://github.com/openxla/stablehlo/blob/main/docs/compatibility.md
  # for the exact extent of these compatibility guarantees.
  #
  # `hlo.get_version_from_compatibility_requirement(WEEK_4)` returns a version
  # of StableHLO >= 4w old. This allows new StableHLO features to be used after
  # ~4w and be compatible with any consumer that is updated on at least a
  # monthly cadence.
  #
  # Note that this does not verify any JAX custom calls, which are only
  # guaranteed 3w of forward compatibility, and only prevents use of new
  # StableHLO features from failing on older hardware.
  target_version = hlo.get_version_from_compatibility_requirement(
    hlo.StablehloCompatibilityRequirement.WEEK_4)

  module_serialized = _jax.mlir.serialize_portable_artifact(
      module, target_version, xb.get_backend().serialize_with_sdy)
  return module_serialized

