import functools
import itertools
import math


def _run_example():
  P = jax.sharding.PartitionSpec
  shape = (4 * 4096, 4 * 4096)  # This shape is global!
  dtype = jnp.bfloat16
  shards = jax.device_count()
  mesh = jax.make_mesh(
      (shards,), ("x",), axis_types=(jax.sharding.AxisType.Explicit,)
  )
  jax.set_mesh(mesh)

  # We measure time per-shard and so we only need bytes per shard.
  local_out_bytes = math.prod(shape) * jnp.dtype(dtype).itemsize
  total_bytes = local_out_bytes

  a = jax.random.normal(jax.random.key(1), shape, dtype)
  a = jax.sharding.reshard(a, P("x", None))

  @jax.jit
  @functools.partial(jax.shard_map, mesh=mesh, in_specs=P("x", None), out_specs=P("x", None))
  def ref_fn(x):
    return lax.all_gather(x, "x", axis=0, tiled=True)
  ref_fn(a).block_until_ready()  # Warmup.
  _, ref_kernels_ms = profiler.measure(ref_fn, aggregate=False)(a)
  assert ref_kernels_ms is not None
  ref_time_us = sum(t * 1e3 for _, t in ref_kernels_ms)
  # We choose the minimum across processes to choose the runtime that didn't
  # include devices waiting for other devices.
  ref_time_us = min(multihost_utils.process_allgather(ref_time_us).tolist())
  ref_bw = total_bytes / (ref_time_us * 1e-6) / 1e9  # GB/s

  tuning_it = itertools.product(
      (4, 8, 16, 32, 64, 132),  # num_blocks
      (1024, 2048, 4096, 8192),  # tile_size
  )
  best_bw = 0.0
  best_runtime = float("inf")
  for num_blocks, tile_size in tuning_it:
    @jax.jit
    @functools.partial(
        jax.shard_map, mesh=mesh, in_specs=P("x", None), out_specs=P("x", None), check_vma=False
    )
    def kernel_fn(x):
      return all_gather(x, axis_name="x", gather_dimension=0, num_blocks=num_blocks, tile_size=tile_size)
    try:
      _, kernels_ms = profiler.measure(kernel_fn, aggregate=False)(a)
    except ValueError as e:
      if "exceeds available shared memory" in e.args[0]:  # Ignore SMEM OOMs.
        continue
      raise
    assert kernels_ms is not None
    runtime_us = sum(t * 1e3 for _, t in kernels_ms)
    runtime_us = min(multihost_utils.process_allgather(runtime_us).tolist())
    achieved_bw = total_bytes / (runtime_us * 1e-6) / 1e9  # GB/s
    if achieved_bw > best_bw:
      best_runtime = runtime_us
      best_bw = achieved_bw
    print(f"{num_blocks=}, {tile_size=}: {runtime_us:<7.1f}us = {achieved_bw:4.1f} GB/s")

  print(f"Total bytes transferred: {total_bytes / 1e9:.2f} GB")
  print(f"\tBest: {best_runtime:<7.1f}us = {best_bw:4.1f} GB/s")
  print(f"\tRef: {ref_time_us:<7.1f}us = {ref_bw:4.1f} GB/s")


def _run_example():
  P = jax.sharding.PartitionSpec
  m_shard = 1024
  n_shard = 4096
  k = 4096
  dtype = jnp.bfloat16
  shards = jax.device_count()
  mesh = jax.make_mesh(
      (shards,), ("x",), axis_types=(jax.sharding.AxisType.Explicit,)
  )
  jax.set_mesh(mesh)

  # We measure time per-shard and so we only need FLOPs per shard.
  matmul_flops = 2 * (shards * m_shard) * n_shard * k
  peak_flops = 990e12  # f16 TensorCore peak = 990 TFLOPS
  optimal_time = matmul_flops / peak_flops * 1e6  # us
  a = jax.random.normal(jax.random.key(1), (shards * m_shard, k), dtype)
  b = jax.random.normal(jax.random.key(2), (k, shards * n_shard), dtype)
  a = jax.sharding.reshard(a, P("x", None))
  b = jax.sharding.reshard(b, P(None, "x"))
  _, ref_kernels_ms = profiler.measure(jax.jit(
      jax.shard_map(
          lambda x, y: lax.all_gather(x, "x", axis=0, tiled=True) @ y,
          out_specs=P(None, "x"),
          check_vma=False,
      )
  ), aggregate=False)(a, b)

  assert ref_kernels_ms is not None
  ref_time_us = _min_results_across_devices(ref_kernels_ms)
  ref_util = optimal_time / ref_time_us * 100

  tuning_it = itertools.product(
      (128, 256,),  # tile_m
      (64, 128),  # tile_n
      (64,),  # tile_k
      (4,),  # max_concurrent_steps
      (MatmulDimension.M, MatmulDimension.N),  # grid_minor_dim
      (4, 8, 16),  # grid_tile_width
      MatmulDimension,  # wg_dimension
  )
  best_util = 0.0
  best_runtime = float("inf")
  def build_kernel(**kwargs):
    return jax.jit(
        jax.shard_map(
            functools.partial(all_gather_lhs_matmul, **kwargs),
            out_specs=P(None, "x"),
            check_vma=False,
        )
    )

  for tile_m, tile_n, tile_k, max_concurrent_steps, grid_minor_dim, grid_tile_width, wg_dimension in tuning_it:
    try:
      config = TuningConfig(
          tile_m=tile_m,
          tile_n=tile_n,
          tile_k=tile_k,
          max_concurrent_steps=max_concurrent_steps,
          grid_minor_dim=grid_minor_dim,
          grid_tile_width=grid_tile_width,
          wg_dimension=wg_dimension,
      )
      _, kernels_ms = profiler.measure(
        build_kernel(axis_name="x", config=config, dtype=dtype),
        aggregate=False,
      )(a, b)
    except ValueError as e:
      if "exceeds available shared memory" in e.args[0]:  # Ignore SMEM OOMs.
        continue
      raise
    assert kernels_ms is not None
    runtime_us = _min_results_across_devices(kernels_ms)
    achieved_tc_util = optimal_time / runtime_us * 100
    if achieved_tc_util > best_util:
      best_runtime = runtime_us
      best_util = achieved_tc_util
    print(
        f"{tile_m=} {tile_n=} {tile_k=} {max_concurrent_steps=} {grid_minor_dim=} {grid_tile_width=} {wg_dimension=}: "
        f"{runtime_us:<7.1f}us"
        f" = {achieved_tc_util:4.1f}% TC utilization"
    )
  print(f"\tBest: {best_runtime:<7.1f}us = {best_util:4.1f}% TC utilization")
  print(f"\tRef: {ref_time_us:<7.1f}us = {ref_util:4.1f}% TC utilization")


def _run_example():
  P = jax.sharding.PartitionSpec
  shape = (4 * 4096, 4 * 4096)  # This shape is global!
  dtype = jnp.bfloat16
  shards = jax.device_count()
  mesh = jax.make_mesh(
      (shards,), ("x",), axis_types=(jax.sharding.AxisType.Explicit,)
  )
  jax.set_mesh(mesh)

  # We measure time per-shard and so we only need bytes per shard.
  local_in_bytes = math.prod(shape) / shards * jnp.dtype(dtype).itemsize
  # In reduce-scatter, we send (shards - 1) / shards worth of input data to the
  # switch and receive as much data as in the whole output, which is 1 / shards.
  total_bytes = local_in_bytes

  a = jax.random.normal(jax.random.key(1), shape, dtype)
  a = jax.sharding.reshard(a, P(None, "x"))

  @jax.jit
  @functools.partial(jax.shard_map, mesh=mesh, in_specs=P(None, "x"), out_specs=P(None, "x"))
  def ref_fn(x):
    return lax.psum_scatter(x, "x", scatter_dimension=1, tiled=True)
  ref_fn(a).block_until_ready()  # Warmup.
  _, ref_kernels_ms = profiler.measure(ref_fn, aggregate=False)(a)
  assert ref_kernels_ms is not None
  ref_time_us = sum(t * 1e3 for _, t in ref_kernels_ms)
  # We choose the minimum across processes to choose the runtime that didn't
  # include devices waiting for other devices.
  ref_time_us = min(multihost_utils.process_allgather(ref_time_us).tolist())
  ref_bw = total_bytes / (ref_time_us * 1e-6) / 1e9  # GB/s

  tuning_it = itertools.product(
      (4, 8, 16, 32, 64, 132),  # num_blocks
      (1024, 2048, 4096, 8192),  # tile_size
  )
  best_bw = 0.0
  best_runtime = float("inf")
  for num_blocks, tile_size in tuning_it:
    try:
      @jax.jit
      @functools.partial(
          jax.shard_map, mesh=mesh, in_specs=P(None, "x"), out_specs=P(None, "x"), check_vma=False
      )
      def kernel_fn(x):
        return reduce_scatter(x, axis_name="x", scatter_dimension=1, num_blocks=num_blocks, tile_size=tile_size)
      kernel_fn(a).block_until_ready()  # Warmup.
      _, kernels_ms = profiler.measure(kernel_fn, aggregate=False)(a)
    except ValueError as e:
      if "exceeds available shared memory" in e.args[0]:  # Ignore SMEM OOMs.
        continue
      raise
    assert kernels_ms is not None
    runtime_us = sum(t * 1e3 for _, t in kernels_ms)
    runtime_us = min(multihost_utils.process_allgather(runtime_us).tolist())
    achieved_bw = total_bytes / (runtime_us * 1e-6) / 1e9  # GB/s
    if achieved_bw > best_bw:
      best_runtime = runtime_us
      best_bw = achieved_bw
    print(f"{num_blocks=}, {tile_size=}: {runtime_us:<7.1f}us = {achieved_bw:4.1f} GB/s")

  print(f"Total bytes transferred: {total_bytes / 1e9:.2f} GB")
  print(f"\tBest: {best_runtime:<7.1f}us = {best_bw:4.1f} GB/s")
  print(f"\tRef: {ref_time_us:<7.1f}us = {ref_bw:4.1f} GB/s")

