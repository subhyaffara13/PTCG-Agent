
def _run_scoped_lowering_rule(ctx, *args, jaxpr, collective_axes, **_):
  if collective_axes:
    raise ValueError(
        "run_scoped lowering outside of Pallas does not support"
        " collective_axes."
    )
  jaxpr_noconst = pe.convert_constvars_jaxpr(jaxpr)
  num_return_values = len(jaxpr_noconst.outvars)
  discharged_closed_body = state_discharge.discharge_state(
      jax_core.ClosedJaxpr(jaxpr_noconst, ()), should_discharge=True)
  discharged_body, new_consts = discharged_closed_body.jaxpr, discharged_closed_body.consts
  if new_consts:
    raise NotImplementedError(
        "Cannot handle new consts created by state discharge.")

  def _lower_fun(*lower_fun_args):
    # Create inputs filled with uninitialized values to the body.
    num_consts = len(lower_fun_args)
    body_avals = [v.aval for v in discharged_body.invars[num_consts:]]
    init_vals = [
        # pyrefly: ignore[missing-attribute]
        uninitialized_value(aval.shape, aval.dtype) for aval in body_avals
    ]
    out = jax_core.eval_jaxpr(discharged_body, [], *lower_fun_args, *init_vals)
    return out[:num_return_values]

  return mlir.lower_fun(_lower_fun, multiple_results=True)(ctx, *args)


def _run_scoped_lowering_rule(
    ctx: LoweringRuleContext, *consts, jaxpr, collective_axes, **_
):
  if collective_axes:
    raise NotImplementedError("run_scoped lowering does not support collective axes")
  region = tpu.RegionOp(map(ctx.aval_to_ir_type, ctx.avals_out))
  in_avals = [v.aval for v in jaxpr.invars]
  with ctx.lowering_context.grid_name_context():
    jaxpr = pe.convert_constvars_jaxpr(jaxpr)
  with ir.InsertionPoint(region.body):
    args = map(lambda aval: _alloc_value(aval, ctx=ctx), in_avals)
    block_shapes = tuple(a.shape if isinstance(a, state.AbstractRef) else None
                         for a in in_avals)
    block_shapes = tuple(map(_maybe_physicalize_block_shape,
                             in_avals, block_shapes))
    lowering_ctx = ctx.lowering_context.replace(
        block_shapes=(*ctx.block_shapes, *block_shapes)
    )
    out = jaxpr_subcomp(lowering_ctx, jaxpr, *consts, *args)
    tpu.yield_(out)
  return region.results


def _run_scoped_lowering_rule(
    ctx: LoweringRuleContext,
    *consts,
    jaxpr: jax_core.Jaxpr,
    collective_axes,
    **_,
):
  if pallas_core.poison_buffers_enabled():
    raise NotImplementedError("Buffer poisoning is not supported on GPU yet.")
  input_refs = []
  should_discharge = []
  wg_axis = ctx.module_ctx.axis_names.wg
  is_multithreaded = wg_axis is not None
  is_thread_collective = is_multithreaded and collective_axes == (wg_axis,)
  # Make sure everyone has exited previous scoped allocations. Note that we
  # don't synchronize when we exit the allocation, but only when we might want
  # to reuse its memory again.
  if collective_axes and collective_axes != (wg_axis,):
    raise ValueError(
        "Only thread-collective allocations are supported in run_scoped."
    )
  if is_multithreaded and is_thread_collective:
    gpu_dialect.barrier()
  with contextlib.ExitStack() as alloc_stack:
    for v in jaxpr.invars:
      aval = cast(ShapedAbstractValue, v.aval)
      if isinstance(aval, gpu_core.WGMMAAbstractAccumulatorRef):
        if collective_axes:
          raise ValueError(
              "WGMMA accumulators can only be allocated non-collectively. Hint:"
              " remove collective_axes from run_scoped. If other allocations"
              " are performed as well, split the run_scoped into two."
          )
        is_signed = mgpu_utils.is_signed(aval.dtype)
        if is_signed is not None and not is_signed:
          raise ValueError(
              "Invalid WGMMA accumulator dtype for s8/i8 WGMMA. "
              f"Expected signed integer, but got {aval.dtype}."
          )

        dtype = mlir.dtype_to_ir_type(aval.dtype)
        if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
          input_refs.append(
              mgpu.WGMMAAccumulator.zero(
                  *aval.shape, dtype=dtype, is_signed=is_signed
              )
          )
        else:
          zero = _ir_constant(0, dtype)
          acc_type = ir.VectorType.get(aval.shape, dtype)
          acc = vector_dialect.broadcast(acc_type, zero)
          acc = mgpu.dialect.optimization_barrier([acc])
          nvvm_dialect.wgmma_fence_aligned()
          input_refs.append(acc)
        should_discharge.append(True)
        continue
      if (
          isinstance(aval, state_types.AbstractRef)
          and aval.memory_space == gpu_core.GMEM
          and jnp.issubdtype(aval.dtype, pallas_core.semaphore)
      ):
        input_ref = alloc_stack.enter_context(
            ctx.module_ctx.reserve_semaphores(
                aval.shape, collective_axes=collective_axes
            )
        )
        input_refs.append(input_ref)
        should_discharge.append(False)
        continue

      # All other allocations must be made collectively across all threads.
      if is_multithreaded and not is_thread_collective:
        raise NotImplementedError(
            "Only thread-collective allocations are supported in multithreaded"
            " kernels. Hint: add"
            f" collective_axes={ctx.module_ctx.axis_names.wg} to your"
            " run_scoped if you intend all threads to share the same"
            f" allocation (currently collective_axes={collective_axes})."
        )
      if isinstance(aval.dtype, gpu_core.BarrierType):
        barrier = _get_barrier(aval, ctx.estimator_ctx.arrival_multiplier)
        barrier_ctx = ctx.module_ctx.reserve_barrier(barrier)
        input_refs.append(alloc_stack.enter_context(barrier_ctx))
        should_discharge.append(False)
        continue
      if isinstance(aval.dtype, gpu_core.ClusterBarrierType):
        barrier = _get_cluster_barrier(aval, ctx.module_ctx.axis_names)
        barrier_ctx = ctx.module_ctx.reserve_barrier(barrier)
        input_refs.append(alloc_stack.enter_context(barrier_ctx))
        should_discharge.append(False)
        continue

      if not isinstance(aval, state_types.AbstractRef):
        raise ValueError(f"Can't convert to ref: {aval}")
      if aval.memory_space == gpu_core.SMEM:
        input_ref = alloc_stack.enter_context(
            ctx.module_ctx.scratch_view(
                jax.ShapeDtypeStruct(shape=aval.shape, dtype=aval.dtype)
            )
        )
        input_refs.append(input_ref)
        should_discharge.append(False)
      elif aval.memory_space == gpu_core.TMEM:
        input_ref = alloc_stack.enter_context(
            ctx.module_ctx.alloc_tmem(
                jax.ShapeDtypeStruct(shape=aval.shape, dtype=aval.dtype),
                layout=aval.layout,  # pyrefly: ignore[missing-attribute]
            )
        )
        input_refs.append(input_ref)
        should_discharge.append(False)

    if any(should_discharge):
      # We convert consts to args, because we only have ir.Values and
      # not JAX values during lowering. discharge_state() produces JAX
      # valiues for the arguments but expects them to be provided for the
      # consts. We also don't want to wrap the values in refs.
      no_const_jaxpr = pe.convert_constvars_jaxpr(jaxpr)
      should_discharge = [False] * len(consts) + should_discharge
      with config._check_vma(False):
        discharged_closed_jaxpr = discharge.discharge_state(
            jax_core.ClosedJaxpr(no_const_jaxpr, ()),
            should_discharge=should_discharge,
        )
        discharged_jaxpr, _ = discharged_closed_jaxpr.jaxpr, discharged_closed_jaxpr.consts
      new_input_vals = (*consts, *input_refs)
      outs = lower_jaxpr_to_mosaic_gpu(
          ctx.module_ctx,
          ctx.launch_ctx,
          discharged_jaxpr,
          new_input_vals,
          (),
      )
      # Discharge appends to the output the refs that got discharged.
      outs = outs[:-sum(should_discharge)]
    else:
      outs = lower_jaxpr_to_mosaic_gpu(
          ctx.module_ctx,
          ctx.launch_ctx,
          jaxpr,
          input_refs,
          consts,
      )

  assert len(outs) == len(jaxpr.outvars), (jaxpr, outs)
  return outs

