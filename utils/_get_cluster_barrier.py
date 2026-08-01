
def _get_cluster_barrier(
    aval: ShapedAbstractValue, axis_names: _AxisNames
) -> mgpu.ClusterBarrier:
  assert isinstance(aval.dtype, gpu_core.ClusterBarrierType)
  num_arrivals = aval.dtype.num_arrivals
  num_barriers = math.prod(aval.shape)
  resolve = functools.partial(_resolve_cluster_axis, axis_names)
  collective_dims = jax.tree.map(resolve, aval.dtype.collective_axes)
  return mgpu.ClusterBarrier(
      collective_dims, num_arrivals, num_barriers,
      orders_tensor_core=aval.dtype.orders_tensor_core,
      leader_tracked=aval.dtype.leader_tracked,
  )

