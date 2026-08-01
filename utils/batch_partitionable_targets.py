
def batch_partitionable_targets() -> list[str]:
  targets = []
  if _cuda_linalg:
    targets.append("cu_lu_pivots_to_permutation")
  if _hip_linalg:
    targets.append("hip_lu_pivots_to_permutation")
  return targets


def batch_partitionable_targets() -> list[str]:
  targets: list[str] = []
  for module in [_cusolver, _hipsolver]:
    if module:
      targets.extend(
          name for name in module.registrations() if name.endswith("_ffi")
      )
  for module in [_cuhybrid, _hiphybrid]:
    if module:
      targets.extend(name for name in module.registrations())
  return targets


def batch_partitionable_targets() -> list[str]:
  targets: list[str] = []
  for module in [_cusparse, _hipsparse]:
    if module:
      targets.extend(
          name for name in module.registrations() if name.endswith("gtsv2_ffi")
      )
  return targets


def batch_partitionable_targets() -> list[str]:
  return [name for name in _lapack.registrations() if name.endswith("_ffi")]

