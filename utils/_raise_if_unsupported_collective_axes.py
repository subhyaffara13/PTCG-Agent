
def _raise_if_unsupported_collective_axes(
    mesh: plgpu.Mesh | None,
    is_collective_by_thread_cluster_axis: tuple[bool, ...],
):
  if not mesh or not mesh.thread_name:
    if any(is_collective_by_thread_cluster_axis):
      raise ValueError(
          "Requesting collective allocations, but no explicit thread axis"
          " specified."
      )
  else:
    # Note that the leading entries in `is_collective_by_thread__cluster_axis`
    # correspond to the cluster axes, while the last entry corresponds to the
    # thread axis within a block.
    *is_collective_by_cluster_axis, is_thread_axis_collective = (
        is_collective_by_thread_cluster_axis
    )
    if any(is_collective_by_cluster_axis):
      raise ValueError(
          "Collective allocations along cluster axes are not supported."
      )
    if not is_thread_axis_collective:
      raise ValueError(
          "Scoped allocation must have the thread axis in its collective axes."
      )

