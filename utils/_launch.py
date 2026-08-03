from typing import Union
import math


def _launch(
    ctx: click.Context, binary: str, args: Sequence[str], *, skip_verify: bool
) -> None:
    base_url = ctx.obj["base_url"]
    started_interactive = _is_interactive()
    api_key = _resolve_api_key(ctx)

    display_name, _ = agent_profile(binary)
    click.echo(
        f"litellm: routing {display_name} through proxy at {base_url.rstrip('/')}"
    )

    try:
        run_agent(
            base_url,
            api_key,
            [binary, *args],
            skip_verify=skip_verify,
            reattach_terminal=(
                _restore_controlling_terminal if started_interactive else None
            ),
        )
    except AgentRunError as e:
        raise click.ClickException(str(e))


def _launch(
    token,
    grid: tuple[int, int, int],
    cluster: tuple[int, int, int],
    block: tuple[int, int, int],
    smem_buffers: ShapeTree | Union[ShapeTree],
    lowering_semantics: LoweringSemantics,
    module: ir.Module,
    inout_buffers_ptr: ir.Value,
    profiler_spec: profiler.ProfilerSpec | None = None,
    maybe_prof_buffer: ir.Value | None = None,
    device_collective_metadata: ir.Value | None = None,
    num_peers: int = 0,
    num_params: int = 0,
):
  if (profiler_spec is None) != (maybe_prof_buffer is None):
    raise ValueError(
        "Both profiler_spec and maybe_prof_buffer must be specified or"
        " left unspecified."
    )
  index = ir.IndexType.get()
  i32 = ir.IntegerType.get_signless(32)
  i8 = ir.IntegerType.get_signless(8)
  grid_vals = [c(i, index) for i in grid]
  block_vals = [c(i, index) for i in block]

  user_smem_bytes = _smem_tree_size(smem_buffers)

  smem_bytes = user_smem_bytes
  if profiler_spec is not None:
    # Profiler array stores values in 64 bit chunks (vectors of size 2
    # of 32-bit elements), and so the starting address needs to be 64
    # bit = 8 byte aligned.
    # https://docs.nvidia.com/cuda/parallel-thread-execution/#addresses-as-operands:~:text=The%20address%20must%20be%20naturally%20aligned%20to%20a%20multiple%20of%20the%20access%20size.
    align = 8
    profiler_start = (smem_bytes + align - 1) & ~(align - 1)
    smem_bytes = profiler_start + profiler_spec.smem_bytes(block=block)

  device = jax.local_devices()[0]
  # For ahead-of-time compilation purposes, that is when a CUDA device
  # isn't available to query directly, we default to 227 KB, the
  # maximum amount of shared memory per thread block available in
  # compute capabilities 9.0 and 10.x:
  # https://docs.nvidia.com/cuda/cuda-c-programming-guide/#features-and-technical-specifications-technical-specifications-per-compute-capability
  # Note in either case we assume all devices have the same amount of
  # shared memory.
  max_smem_bytes = getattr(device, "shared_memory_per_block_optin", 227 * 1024)
  if _SMEM_SIZE_BOUND is not None:
    max_smem_bytes = min(max_smem_bytes, _SMEM_SIZE_BOUND)
  if smem_bytes > max_smem_bytes:
    raise ValueError("Mosaic GPU kernel exceeds available shared memory: "
                     f"{smem_bytes=} > {max_smem_bytes=}")
  if math.prod(cluster) != 1:
    if len(cluster) != 3:
      raise ValueError(f"Clusters must be 3D. Got: {cluster}")
    cluster_kwargs = {
        "clusterSize" + d: c(s, index) for s, d in zip(cluster, "XYZ")
    }
    for d, grid_size, cluster_size in zip("xyz", grid, cluster):
      if grid_size % cluster_size != 0:
        raise ValueError(
            f"Grid dimension {d} must be divisible by cluster dimension:"
            f" {grid_size} % {cluster_size} != 0"
        )
  else:
    cluster_kwargs = {}
  # `gpu.LaunchOp` is missing the clusterSize{X,Y,Z} arguments.
  launch_op = _gpu_ops_gen.LaunchOp(
      token.type,
      [token],
      *grid_vals,
      *block_vals,
      dynamicSharedMemorySize=c(smem_bytes, i32),
      **cluster_kwargs,
  )
  launch_op.body.blocks.append(*([index] * (12 + 2 * len(cluster_kwargs))))  # Append an empty block
  with ir.InsertionPoint(launch_op.body.blocks[0]):
    dynamic_smem = gpu.dynamic_shared_memory(
        ir.MemRefType.get((utils.DYNAMIC,), i8, memory_space=utils.smem())
    )

    if profiler_spec:
      prof_smem = _slice_smem(
          ir.MemRefType.get(
              (profiler_spec.smem_i32_elements(block=block),),
              i32,
              memory_space=utils.smem(),
          ),
          dynamic_smem,
          profiler_start,  # pyrefly: ignore[unbound-name]
          lowering_semantics,
      )
      if lowering_semantics == LoweringSemantics.Warpgroup:
        prof_smem = dialect.with_transforms(prof_smem, ir.ArrayAttr.get([]))
        wrap_in_custom_primitive = True
      else:
        wrap_in_custom_primitive = False
      assert maybe_prof_buffer is not None
      prof = profiler.OnDeviceProfiler(
          profiler_spec,
          prof_smem,
          maybe_prof_buffer,
          wrap_in_custom_primitive,
      )
    else:
      prof = None

    ctx = launch_context.LaunchContext(
        module,
        launch_context.Scratch(launch_op),
        cluster,
        inout_buffers_ptr,
        prof,
        device_collective_metadata=device_collective_metadata,
        num_peers=num_peers,
        num_params=num_params,
        num_processes=jax.process_count(),
    )
    with ctx.named_region("Init"):
      tmem_allocs: list[_TMEMAlloc | _TMEMDialectAlloc] = []
      smem_ref_tree_thunk = _construct_smem_reftree(
          cluster, dynamic_smem, smem_buffers, tmem_allocs, lowering_semantics
      )
      # TODO(apaszke): Skip fences if no barriers or TMEM is initialized.
      # TODO(apaszke): Only initialize cluster barriers before the cluster wait.
      nvvm.fence_mbarrier_init()
      if math.prod(cluster) != 1:
        nvvm.cluster_arrive_relaxed(aligned=True)
        nvvm.cluster_wait(aligned=True)
      if tmem_allocs:
        init_warp_ctx: contextlib.AbstractContextManager
        if lowering_semantics == LoweringSemantics.Warpgroup:
          init_warp_ctx = contextlib.nullcontext()
        else:
          eq = arith.CmpIPredicate.eq
          is_init_warp = arith.cmpi(eq, utils.warp_idx(sync=False), c(0, i32))
          init_warp_ctx = utils.when(is_init_warp)
        with init_warp_ctx:
          cols_used = 0
          for alloc in tmem_allocs:
            cols_used += alloc.alloc()
          if cols_used > tcgen05.TMEM_MAX_COLS:
            raise ValueError(
                "Total TMEM allocation exceeds memory limit. "
                f"Requested {cols_used} columns which exceeds limit of "
                f"{tcgen05.TMEM_MAX_COLS}."
            )
          collective_types = {alloc.collective for alloc in tmem_allocs}
          if len(collective_types) > 1:
            raise ValueError(
                "Can't mix collective and non-collective TMEM allocations"
                " within the same kernel."
            )
          collective = True in collective_types
          if collective and math.prod(cluster) % 2:
            raise ValueError(
                "Collective TMEM allocations are only supported for clusters"
                " with an even number of blocks in them. Got cluster:"
                f" {cluster}"
            )
          if lowering_semantics == LoweringSemantics.Warpgroup:
            dialect.tmem_relinquish_alloc_permit(collective=collective)
          else:
            tcgen05.tmem_relinquish_alloc_permit(collective=collective)
      gpu.barrier()  # Make sure the init is visible to all threads.
      smem_ref_tree = smem_ref_tree_thunk()

    yield ctx, smem_ref_tree

    if tmem_allocs:
      gpu.barrier()  # Make sure everyone is done before we release TMEM.
      if any(alloc.collective for alloc in tmem_allocs):
        nvvm.cluster_arrive_relaxed(aligned=True)
        nvvm.cluster_wait(aligned=True)
      if lowering_semantics == LoweringSemantics.Warpgroup:
        init_warp_ctx = contextlib.nullcontext()
      else:
        init_warp_ctx = utils.when(is_init_warp)  # pyrefly: ignore[unbound-name]
      with init_warp_ctx:
        for alloc in tmem_allocs:
          alloc.dealloc()
    if prof is not None:
      prof.finalize(grid=grid, block=block)
    gpu.terminator()

