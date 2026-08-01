
def _run_state_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    jaxpr: jax_core.Jaxpr,
    which_linear: tuple[bool, ...],
    is_initialized: tuple[bool, ...],
):
  del which_linear
  # TODO(apaszke): This should be unified with run_scoped.
  if not all(is_initialized):
    raise NotImplementedError("Uninitialized Refs are not supported in lowering of run_state.")

  should_discharge = []
  new_input_vals = []
  for arg, v, out_aval in zip(args, jaxpr.invars, ctx.avals_out):
    aval = v.aval
    if isinstance(aval, gpu_core.WGMMAAbstractAccumulatorRef):
      if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
        arg = mgpu.dialect.optimization_barrier([arg])
        nvvm_dialect.wgmma_fence_aligned()
        new_input_vals.append(arg)
      else:
        new_input_vals.append(mgpu.WGMMAAccumulator.from_registers(arg))
      should_discharge.append(True)
      assert isinstance(out_aval, jax_core.ShapedArray)
    else:
      new_input_vals.append(arg)
      should_discharge.append(not isinstance(out_aval, state_types.AbstractRef))
  if not any(should_discharge):
    raise NotImplementedError(
        "Expected at least one accumulator to in run_state."
    )

  with config._check_vma(False):
    discharged_closed_jaxpr = discharge.discharge_state(
        jax_core.ClosedJaxpr(jaxpr, ()), should_discharge=should_discharge
    )
    discharged_jaxpr, new_consts = discharged_closed_jaxpr.jaxpr, discharged_closed_jaxpr.consts
  assert not new_consts
  outs = lower_jaxpr_to_mosaic_gpu(
      ctx.module_ctx, ctx.launch_ctx, discharged_jaxpr, new_input_vals, ()  # pyrefly: ignore[bad-argument-type]
  )
  # Await the accumulators and extract their final values.
  nvvm_dialect.wgmma_wait_group_sync_aligned(0)
  outs = [
      out.value if isinstance(out, mgpu.WGMMAAccumulator) else out
      for out in outs
  ]
  # Blend the discharge results with refs we closed over. I don't fully
  # understand the reasons behind this calling convention, but sharadmv@ has
  # assured me that this is ok.
  outs_it = iter(outs)
  return [next(outs_it) if d else a for d, a in zip(should_discharge, args)]

