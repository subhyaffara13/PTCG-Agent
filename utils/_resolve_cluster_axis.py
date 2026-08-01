
def _resolve_cluster_axis(axis_names: _AxisNames | None, axis_name: Hashable):
  if not axis_names:
    raise LookupError(
        "No axis names are available. Make sure you are using `pl.core_map`"
        " with a `plgpu.Mesh`."
    )
  if not axis_names or axis_name not in axis_names.cluster:
    raise LookupError(
        f"Unknown cluster axis {axis_name}, available axes:"
        f" {[*axis_names.cluster]}"
    )
  return gpu_dialect.Dimension(axis_names.cluster.index(axis_name))

