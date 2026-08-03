import math


def _check_divisibility(sharding, shape):
  mesh = sharding.mesh
  for dim, (spec, sh) in enumerate(zip(sharding.spec.partitions, shape)):
    if spec is None:
      continue
    spec = spec if isinstance(spec, tuple) else (spec,)
    size = math.prod(mesh.shape[s] for s in spec)
    _, remainder = divmod(sh, size)
    if remainder != 0:
      raise ValueError(
          f"Sharding spec {spec} implies that array axis {dim} is partitioned"
          f" {size} times, but does not evenly divide the dimension size {sh}."
          f" Got shape: {shape} and sharding {sharding}")

