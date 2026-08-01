
def _run_scoped_resource_estimator(
    ctx: ResourceEstimatorContext,
    *consts,
    jaxpr: jax_core.Jaxpr,
    collective_axes,
    **_,
) -> Resources:
  # NOTE: This rule assumes that the allocation happens collectively, although
  # it can't be checked here due to limited context. We check this in the actual
  # lowering rule.
  del consts  # Unused.
  rs = Resources()
  for v in jaxpr.invars:
    aval = cast(ShapedAbstractValue, v.aval)
    if isinstance(aval.dtype, gpu_core.BarrierType):
      barrier = _get_barrier(aval, ctx.arrival_multiplier)
      rs += Resources(barrier_counts=collections.Counter([barrier]))
      continue
    if isinstance(aval.dtype, gpu_core.ClusterBarrierType):
      barrier = _get_cluster_barrier(aval, ctx.axis_names)
      rs += Resources(barrier_counts=collections.Counter([barrier]))
      continue
    assert isinstance(aval, state_types.AbstractRef)
    if aval.memory_space == gpu_core.TMEM:
      if len(aval.shape) != 2:
        raise ValueError(f"TMEM allocations must be 2D. Got {aval.shape}")
      # Estimate columns used.
      if isinstance(aval, gpu_core.AbstractRefUnion):
        assert aval.shape[0] == 128
        cols_used = aval.shape[1]
      else:
        # pyrefly: ignore[missing-attribute]
        cols_used = aval.layout.cols_in_shape(
            aval.shape, dtypes.itemsize_bits(aval.dtype)
        )
      if aval.collective:  # pyrefly: ignore[missing-attribute]
        rs += Resources(tmem_collective_scratch_cols=cols_used)
      else:
        rs += Resources(tmem_scratch_cols=cols_used)
    elif aval.memory_space == gpu_core.SMEM:
      rs += Resources(
          smem_scratch_bytes=aval.size * dtypes.itemsize_bits(aval.dtype) // 8
      )
    elif aval.memory_space == gpu_core.REGS:
      # Don't need to allocate anything.
      pass
    elif aval.memory_space == gpu_core.GMEM and jnp.issubdtype(aval.dtype, pallas_core.semaphore):
      if _is_block_local_scope(collective_axes, ctx.axis_names):
        rs += Resources(scoped_gmem_semaphores={collective_axes: aval.size})
      else:
        raise ValueError(
            "Only thread-collective allocations are supported in run_scoped. To"
            " allocate global semaphores, use pl.get_global."
        )
    else:
      raise NotImplementedError(
          f"Unsupported memory space: {aval.memory_space}")
  return rs + _estimate_resources(ctx, jaxpr)

