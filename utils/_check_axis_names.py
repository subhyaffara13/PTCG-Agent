
def _check_axis_names(axes, api_name):
  named_axes = tuple(axis for axis in axes if not isinstance(axis, int))
  axis_env = core.get_axis_env()
  for name in named_axes:
    if not axis_env.axis_exists(name):
      raise NameError(
          f"Found an unbound axis name: {name}. To fix this, please call"
          f" {api_name} under `jax.shard_map`.")

