
def collective_vma_rule(prim_name, axis_name, x_aval):
  if not config._check_vma.value:
    return frozenset()
  axis_name = (axis_name,) if not isinstance(axis_name, tuple) else axis_name
  if any(a not in x_aval.mat.varying for a in axis_name):
    raise ValueError(
        f"Collective {prim_name} must be applied to a device-varying "
        f" type, but got {x_aval.mat.varying} for collective acting "
        f"over axis name {axis_name}. Please open an issue at "
        "https://github.com/jax-ml/jax/issues and as a temporary "
        "workaround pass the check_vma=False argument to `jax.shard_map`")
  return x_aval.mat.varying

