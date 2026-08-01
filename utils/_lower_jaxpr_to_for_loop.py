
def _lower_jaxpr_to_for_loop(ctx: LoweringRuleContext,
                             jaxpr: jax_core.Jaxpr, start: int | ir.Value,
                             num_steps: int | ir.Value, consts, *args,
                             has_loop_index: bool,
                             unroll: int):
  is_static_start = not isinstance(start, ir.Value)
  is_static_steps = not isinstance(num_steps, ir.Value)

  if unroll == 0:
    if is_static_steps:
      unroll = num_steps
    else:
      raise ValueError(
        "Cannot fully unroll loop with dynamic number of steps (unroll=0)")

  if unroll > 1:
    const_types = [val.type for val in consts]
    args_types = [val.type for val in args]

    user_grid_indices = ctx.lowering_context.user_grid_indices
    has_grid = user_grid_indices is not None
    grid_arity = len(user_grid_indices) if has_grid else 0

    func_arg_types = []
    if has_grid:
      func_arg_types.extend(val.type for val in user_grid_indices)
    func_arg_types.extend(const_types)
    if has_loop_index:
      func_arg_types.append(_dtype_to_ir_type(jnp.int32))
    func_arg_types.extend(args_types)

    def body_builder(block_args: list[ir.Value]) -> list[ir.Value]:
      if has_grid:
        block_grid_indices = block_args[:grid_arity]
        block_rest = block_args[grid_arity:]
      else:
        block_grid_indices = None
        block_rest = block_args

      lowering_context = ctx.lowering_context.replace(
          block_shapes=ctx.block_shapes,
          user_grid_indices=block_grid_indices,
      )
      return jaxpr_subcomp(lowering_context, jaxpr, *block_rest)

    func_op = _emit_detached_func(
        "_unrolled_loop_body",
        func_arg_types,
        args_types,
        body_builder
    )

    def _run_body(i, args):
      call_args = []
      if has_grid:
        call_args.extend(user_grid_indices)
      call_args.extend(consts)
      if has_loop_index:
        call_args.append(i)
      call_args.extend(args)
      outs = jax_mlir_ext.inlined_func_call(func_op.operation, call_args)
      return outs
  else:
    def _run_body(i, args):
      lowering_context = ctx.lowering_context.replace(
          block_shapes=ctx.block_shapes)
      if has_loop_index:
        args = jaxpr_subcomp(lowering_context, jaxpr, *consts, i, *args)
      else:
        args = jaxpr_subcomp(lowering_context, jaxpr, *consts, *args)
      return args

  if is_static_start and is_static_steps and num_steps == unroll:
    # No need for an scf.For. We can just unroll completely
    for i in range(start, start + num_steps):
      args = _run_body(
          ir_constant(i, mlir_type=_dtype_to_ir_type(jnp.int32)), args
      )
    return args

  lbd = _ensure_mlir_value(start, pallas_core.index_map_grid_aval)
  remainder = 0
  main_range = 0
  ubd = lbd

  if is_static_steps:
    num_steps_int = cast(int, num_steps)
    main_steps = num_steps_int // unroll
    remainder = num_steps_int % unroll

    main_range = main_steps * unroll
    main_ubd = arith.addi(
        lbd, ir_constant(main_range, mlir_type=_dtype_to_ir_type(jnp.int32))
    )

    has_main = main_steps > 0
    has_static_remainder = remainder > 0
    has_dynamic_remainder = False
  else:
    num_steps_val = _ensure_mlir_value(
        num_steps, pallas_core.index_map_grid_aval
    )
    ubd = arith.addi(lbd, num_steps_val)

    unroll_val = ir_constant(unroll, mlir_type=_dtype_to_ir_type(jnp.int32))
    main_steps_val = arith.divsi(num_steps_val, unroll_val)
    main_range_val = arith.muli(main_steps_val, unroll_val)
    main_ubd = arith.addi(lbd, main_range_val)

    has_main = True
    has_static_remainder = False
    has_dynamic_remainder = True

  if has_main:
    step_val = ir_constant(unroll, mlir_type=_dtype_to_ir_type(jnp.int32))
    main_for_op = scf.ForOp(lbd, main_ubd, step_val, args)
    with ir.InsertionPoint(main_for_op.body):
      iv = main_for_op.induction_variable
      inner_args = main_for_op.inner_iter_args

      loop_args = inner_args
      for step_idx in range(unroll):
        if step_idx == 0:
          actual_i = iv
        else:
          actual_i = arith.addi(
              iv,
              ir_constant(step_idx, mlir_type=_dtype_to_ir_type(jnp.int32)),
          )
        loop_args = _run_body(actual_i, loop_args)
      scf.yield_(loop_args)
    args = main_for_op.results

  if has_static_remainder:
    for i in range(remainder):
      actual_i = arith.addi(
          lbd,
          ir_constant(
              main_range + i, mlir_type=_dtype_to_ir_type(jnp.int32)
          ),
      )
      args = _run_body(actual_i, args)

  elif has_dynamic_remainder:
    one_val = ir_constant(1, mlir_type=_dtype_to_ir_type(jnp.int32))
    rem_for_op = scf.ForOp(main_ubd, ubd, one_val, args)
    with ir.InsertionPoint(rem_for_op.body):
      iv = rem_for_op.induction_variable
      inner_args = rem_for_op.inner_iter_args
      inner_out = _run_body(iv, inner_args)
      scf.yield_(inner_out)
    args = rem_for_op.results

  return args


def _lower_jaxpr_to_for_loop(
    ctx: LoweringRuleContext,
    jaxpr: jax_core.Jaxpr,
    start: ir.Value,
    length: int | ir.Value,
    consts,
    *args,
    has_loop_index: bool,
    unroll: int | None = None,
):
  _consts_avals, arg_avals = util.split_list(ctx.avals_in, [len(consts)])
  arg_avals = arg_avals[has_loop_index:]
  out_avals = []
  if arg_avals:
    out_avals = ctx.avals_out[-len(arg_avals):]

  is_acc = [isinstance(v, mgpu.WGMMAAccumulator) for v in args]
  def as_values(vals, avals):
    if is_acc != [isinstance(v, mgpu.WGMMAAccumulator) for v in vals]:
      raise ValueError("Unexpected loop carry w.r.t. accumulators.")

    _ensure = (
        _ensure_fa
        if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane
        else _ensure_ir_value
    )
    return [
        v if a else _ensure(v, av.dtype)
        for a, v, av in zip(is_acc, vals, avals)
    ]

  def loop(base_loop_index, body_args):
    outs = body_args
    if unroll is not None:
      base_loop_index = arith_dialect.muli(
          base_loop_index, _ir_constant(unroll, start.type)
      )
    base_loop_index = arith_dialect.addi(base_loop_index, start)
    for step in range(unroll or 1):
      if has_loop_index:
        loop_index = arith_dialect.addi(
            base_loop_index, _ir_constant(step, start.type)
        )
        jaxpr_args = [*consts, loop_index, *outs]
      else:
        jaxpr_args = [*consts, *outs]
      outs = lower_jaxpr_to_mosaic_gpu(
          ctx.module_ctx, ctx.launch_ctx, jaxpr, jaxpr_args
      )
    return as_values(outs, out_avals)

  if unroll is not None:
    if not isinstance(length, int):
      raise NotImplementedError(
          "``length`` must be an integer when ``unroll` is specified, got"
          f" {length}"
      )
    if length % unroll:
      # TODO(slebedev): Emit an epilogue taking care of the remaining steps.
      raise NotImplementedError(
          f"``unroll`` must divide ``length``, got {unroll=} and {length=}"
      )
    if unroll == length:
      # Special-case: the loop is fully unrolled.
      return loop(_ir_constant(0, start.type), as_values(args, arg_avals))
    return mgpu.fori(
        _ir_constant(length // unroll, start.type), as_values(args, arg_avals)
    )(loop).results
  else:
    if not isinstance(length, ir.Value):
      length = _ir_constant(length, start.type)
    return mgpu.fori(length, as_values(args, arg_avals))(loop).results


def _lower_jaxpr_to_for_loop(
    ctx: LoweringRuleContext,
    jaxpr: jax_core.Jaxpr,
    lower_bound,
    upper_bound,
    consts,
    *args,
    has_loop_index: bool,
    step: int = 1,
    bound_type: ir.IntegerType | None = None,
):
  if step != 1:
    raise NotImplementedError
  if bound_type is None or bound_type.width == 32:
    step_val = _i32_constant(step)
  else:
    step_val = _i64_constant(step)

  for_op = scf_dialect.ForOp(lower_bound, upper_bound, step_val, args)
  with ir.InsertionPoint.at_block_begin(for_op.body):
    loop_index = for_op.induction_variable
    for_body_args = [for_op.body.arguments[i + 1] for i, _ in enumerate(args)]
    if has_loop_index:
      jaxpr_args = [*consts, loop_index, *for_body_args]
    else:
      jaxpr_args = [*consts, *for_body_args]
    all_out = lower_jaxpr_to_triton_ir(
        ctx.context, jaxpr, ctx.block_infos, *jaxpr_args
    )
    scf_dialect.yield_(all_out)

  return list(for_op.results_)

