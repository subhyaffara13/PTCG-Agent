
def lower_jaxpr_to_fun(
    ctx: ModuleContext,
    name: str,
    jaxpr: core.ClosedJaxpr,
    effects: Sequence[core.Effect],
    *,
    num_const_args: int,
    main_function: bool = False,
    replicated_args: Sequence[bool] | None = None,
    in_avals: Sequence[core.AbstractValue],
    arg_shardings: Sequence[JSharding | None] | None = None,
    result_shardings: Sequence[JSharding | None] | None = None,
    use_sharding_annotations: bool = True,
    input_output_aliases: Sequence[int | None] | None = None,
    xla_donated_args: Sequence[bool] | None = None,
    arg_names: Sequence[str | None] | None = None,
    result_names: Sequence[str] | None = None,
    arg_memory_kinds: Sequence[str | None] | None = None,
    result_memory_kinds: Sequence[str | None] | None = None,
    arg_layouts: Sequence[Layout | None | AutoLayoutSingleton] | None = None,
    result_layouts: Sequence[Layout | None | AutoLayoutSingleton] | None = None,
    propagated_out_mem_kinds: tuple[None | str, ...] | None = None,
) -> func_dialect.FuncOp:
  """Lowers jaxpr and its callees to an IR function.

  Assumes that an MLIR context, location, and insertion point are set.

  Note: this function does *not* take a name stack. Name stacks do not cross
  the boundaries of HLO functions.

  Args:
    ctx: the lowering context.
    name: the function name. The name will be uniquified by the symbol table,
      so it is ok to use the same name multiple times.
    jaxpr: the jaxpr to lower.
    effects: a sequence of `core.Effect`s corresponding to an ordering of tokens
      that will be created in or used by the lowered function.
    num_const_args: how many constant arguments is this function going to have.
      See https://docs.jax.dev/en/latest/internals/constants.html
    main_function: if true, this is the main function in the module. This has
      several effects:
      * the function's visibility is set to "public".
      * the function's symbol name will be "main"
      * the function's name will be used as the root name stack entry.
    replicated_args: if present, annotates arguments as replicated.
    arg_shardings: sharding annotations for each argument (optional).
    result_shardings: sharding annotations for each result (optional).
    use_sharding_annotations: if True, use "mhlo.sharding" annotations on
      parameters and return values to express sharding. If False, use
      hlo.custom_call operators with sharding annotations.
      TODO(b/228598865): remove this option when "mhlo.sharding" annotations are
      propagated on non-entry functions during MLIR->HLO conversion.
    input_output_aliases: optional sequence that maps argument numbers to the
      corresponding output that should alias them.
    xla_donated_args: optional sequence of args to set donation annotations.
  Returns:
    MLIR func op
  """
  util.test_event("lower_jaxpr_to_fun", name)
  if not config.use_simplified_jaxpr_constants.value:
    check_jaxpr_constants(jaxpr)

  # The first dimension variable may be the platform index
  num_dim_vars = len(ctx.shape_poly_state.dim_vars)
  dim_var_avals = [core.ShapedArray((), dtypes.default_int_dtype())] * num_dim_vars
  dim_var_types = [aval_to_ir_type(ctx, aval) for aval in dim_var_avals]

  nr_args = num_const_args + len(jaxpr.in_avals)

  assert nr_args == len(in_avals), (nr_args, in_avals)
  assert replicated_args is None or nr_args == len(replicated_args), \
    (nr_args, replicated_args)
  assert arg_shardings is None or nr_args == len(arg_shardings), \
    (nr_args, arg_shardings)
  assert arg_layouts is None or nr_args == len(arg_layouts), \
    (nr_args, arg_layouts)
  assert arg_memory_kinds is None or nr_args == len(arg_memory_kinds), \
    (nr_args, arg_memory_kinds)
  assert arg_names is None or nr_args == len(arg_names), (nr_args, arg_names)

  # Function inputs: *dim_var_values, *tokens, *const_args, *actual_inputs
  input_types = [_aval_to_ir_types(ctx, a) for a in in_avals]
  output_types = [_aval_to_ir_types(ctx, a) for a in jaxpr.out_avals]
  num_tokens = len(effects)

  token_types = [token_type() for _ in effects]
  token_avals = [core.abstract_token] * num_tokens
  # Order of arguments: dim vars, tokens, const_args, array inputs
  input_avals = dim_var_avals + token_avals + list(in_avals)
  input_types = [*dim_var_types, *token_types, *input_types]
  output_avals = [core.abstract_token] * num_tokens + jaxpr.out_avals
  output_types = [*token_types, *output_types]

  if input_output_aliases is not None:
    prefix_input_output_aliases = [None] * (num_dim_vars + num_tokens)
    input_output_aliases = [*prefix_input_output_aliases, *input_output_aliases]
    # Update the existing aliases to account for the new output values
    input_output_aliases = [None if a is None
                            else a + num_tokens
                            for a in input_output_aliases]

  if arg_shardings is not None:
    prefix_shardings = [None] * (num_dim_vars + num_tokens)
    arg_shardings = [*prefix_shardings, *arg_shardings]
  if result_shardings is not None:
    token_shardings = [None] * num_tokens
    result_shardings = [*token_shardings, *result_shardings]
  if replicated_args is not None:
    prefix_replicated_args = [False] * (num_dim_vars + num_tokens)
    replicated_args = [*prefix_replicated_args, *replicated_args]
  if arg_memory_kinds is not None:
    prefix_memory_kinds = [None] * (num_dim_vars + num_tokens)
    arg_memory_kinds = [*prefix_memory_kinds, *arg_memory_kinds]
  if result_memory_kinds is not None:
    token_memory_kinds = [None] * num_tokens
    result_memory_kinds = [*token_memory_kinds, *result_memory_kinds]
  if arg_layouts is not None:
    prefix_layouts = [None] * (num_dim_vars + num_tokens)
    arg_layouts = [*prefix_layouts, *arg_layouts]
  if result_layouts is not None:
    token_layouts = [None] * num_tokens
    result_layouts = [*token_layouts, *result_layouts]
  if xla_donated_args is not None:
    xla_donated_args = [*([False] * (num_dim_vars + num_tokens)),
                        *xla_donated_args]

  flat_input_types, input_types_treedef = ir_tree_registry.flatten(input_types)
  flat_output_types, _ = ir_tree_registry.flatten(output_types)
  ftype = ir.FunctionType.get(flat_input_types, flat_output_types)
  func_name = "main" if main_function else name
  func_op = func_dialect.FuncOp(func_name, ftype, ip=ctx.ip)
  func_op.attributes["sym_visibility"] = ir.StringAttr.get(
      "public" if main_function else "private")
  ctx.symbol_table.insert(func_op)

  ir_arg_shardings = None
  if arg_shardings is not None:
    ir_arg_shardings = util.flatten(
        [[_to_physical_op_sharding(ctx, a, s)] * len_ir_types(types)
         for a, s, types in zip(input_avals, arg_shardings, input_types)])

  ir_arg_memory_kinds = None
  if arg_memory_kinds is not None:
    ir_arg_memory_kinds = util.flatten(
        [[mk] * len_ir_types(types)
         for mk, types in zip(arg_memory_kinds, input_types)])

  ir_arg_layouts = None
  if arg_layouts is not None:
    ir_arg_layouts = util.flatten(
        [[_to_xla_layout(l, a)] * len_ir_types(types)
         for l, a, types in zip(arg_layouts, input_avals, input_types)])

  ir_donated_args = None
  if xla_donated_args is not None:
    ir_donated_args = util.flatten(
        [[is_donated] * len_ir_types(types)
         for is_donated, types in zip(xla_donated_args, input_types)])

  ir_result_shardings = None
  sharding_contains_unconstrained = None
  if result_shardings is not None:
    ir_result_shardings = util.flatten(
        [[_to_physical_op_sharding(ctx, a, s)] * len_ir_types(types)
         for a, s, types in zip(output_avals, result_shardings, output_types)])
    sharding_contains_unconstrained = util.flatten(
        [[contains_unconstrained(s)] * len_ir_types(types)
         for s, types in zip(result_shardings, output_types)])

  ir_result_memory_kinds = None
  custom_call_ir_result_memory_kinds = None
  if result_memory_kinds is not None:
    if propagated_out_mem_kinds is None:
      propagated_out_mem_kinds = (None,) * len(result_memory_kinds)
    res, custom_call_res = [], []
    for pom, mk, types in zip(propagated_out_mem_kinds, result_memory_kinds,
                              output_types):
      if pom is not None and mk is None:
        res.append([pom] * len_ir_types(types))
      else:
        res.append([mk] * len_ir_types(types))
      # To add the custom call on the output to signal a transfer, only do it
      # if memory kind comes from out_shardings on `jit` and result_memory_kinds
      # comes from out_shardings on `jit`.
      custom_call_res.append([mk] * len_ir_types(types))
    ir_result_memory_kinds = util.flatten(res)
    custom_call_ir_result_memory_kinds = util.flatten(custom_call_res)

  ir_result_layouts = None
  if result_layouts is not None:
    ir_result_layouts = util.flatten(
        [[_to_xla_layout(l, a)] * len_ir_types(types)
         for l, a, types in zip(result_layouts, output_avals, output_types)])

  # Populate arg_attrs
  if (
      replicated_args is not None
      or ir_arg_shardings is not None
      or ir_arg_memory_kinds is not None
      or ir_arg_layouts is not None
      or input_output_aliases is not None
      or ir_donated_args is not None
      or arg_names is not None
      or num_tokens > 0
      or num_dim_vars > 0
      or num_const_args > 0
  ):
    arg_attrs: list[dict[str, ir.Attribute]] = [
        {} for _ in range(len(flat_input_types))]

    if replicated_args is not None:
      replicated_ir_args = [[replicated] * len_ir_types(types) for replicated, types
                            in zip(replicated_args, input_types)]
      for attrs, replicated in zip(arg_attrs, util.flatten(replicated_ir_args)):
        if replicated:
          attrs["mhlo.is_same_data_across_replicas"] = ir.BoolAttr.get(True)

    if use_sharding_annotations and ir_arg_shardings is not None:
      for attrs, sharding in zip(arg_attrs, ir_arg_shardings):
        if sharding is not None:
          if config.use_shardy_partitioner.value:
            attrs["sdy.sharding"] = get_sharding_attr(ctx, sharding)
          else:
            attrs["mhlo.sharding"] = get_sharding_attr(ctx, sharding)

    if ir_arg_memory_kinds is not None:
      for attrs, memory_kind in zip(arg_attrs, ir_arg_memory_kinds):
        if memory_kind is not None:
          attrs["mhlo.memory_kind"] = ir.StringAttr.get(memory_kind)

    if ir_arg_layouts is not None:
      for attrs, layout in zip(arg_attrs, ir_arg_layouts):
        if layout is not None:
          attrs["mhlo.layout_mode"] = ir.StringAttr.get(layout)

    if ir_donated_args is not None:
      for attrs, is_donated in zip(arg_attrs, ir_donated_args):
        if is_donated:
          attrs["jax.buffer_donor"] = ir.BoolAttr.get(True)

    if input_output_aliases is not None:
      output_ids = util.unflatten(
        list(range(len(flat_output_types))), map(len_ir_types, output_types))
      aliases: list[int | None] = []
      for itypes, alias in zip(input_types, input_output_aliases):
        if alias is None:
          aliases.extend([None] * len_ir_types(itypes))
        else:
          aliases.extend(output_ids[alias])
      for attrs, alias in zip(arg_attrs, aliases):
        if alias is not None:
          attrs["tf.aliasing_output"] = i32_attr(alias)

    if num_dim_vars > 0:
      for var_name, attrs in zip(ctx.shape_poly_state.dim_vars,
                                 arg_attrs[:num_dim_vars]):
        attrs["jax.global_constant"] = ir.StringAttr.get(var_name)
    elif ctx.lowering_parameters.global_constant_computation:
      for attrs in arg_attrs:
        attrs["jax.global_constant"] = ir.StringAttr.get("")

    if num_tokens > 0:
      token_arg_attrs = arg_attrs[num_dim_vars:num_dim_vars + num_tokens]
      for attrs in token_arg_attrs:
        attrs["jax.token"] = ir.BoolAttr.get(True)

    if num_const_args > 0:
      const_arg_attrs = arg_attrs[num_dim_vars + num_tokens :
                                  num_dim_vars + num_tokens + num_const_args]
      for attrs in const_arg_attrs:
        attrs["jax.const"] = ir.BoolAttr.get(True)

    func_op.arg_attrs = ir.ArrayAttr.get(
        [ir.DictAttr.get(attrs) for attrs in arg_attrs])
    # End populate arg_attrs

  result_attrs: list[dict[str, ir.Attribute]] = [
      {} for _ in range(len(flat_output_types))]

  if num_tokens > 0:
    token_result_attrs = result_attrs[:num_tokens]
    for attrs in token_result_attrs:
      attrs["jax.token"] = ir.BoolAttr.get(True)

  if result_names:
    named_result_attrs = result_attrs[num_tokens:]
    if len(named_result_attrs) == len(result_names):
      for attrs, name_ in zip(named_result_attrs, result_names):
        attrs['jax.result_info'] = ir.StringAttr.get(name_)

  if use_sharding_annotations and ir_result_shardings is not None:
    for attrs, sharding, cu in zip(result_attrs, ir_result_shardings,
                                   sharding_contains_unconstrained):  # type: ignore
      if sharding is not None and not cu:
        if config.use_shardy_partitioner.value:
          attrs["sdy.sharding"] = get_sharding_attr(ctx, sharding)
        else:
          attrs["mhlo.sharding"] = get_sharding_attr(ctx, sharding)

  if ir_result_memory_kinds is not None:
    for attrs, mem_kind in zip(result_attrs, ir_result_memory_kinds):
      if mem_kind is not None:
        attrs['mhlo.memory_kind'] = ir.StringAttr.get(mem_kind)

  if ir_result_layouts is not None:
    for attrs, layout in zip(result_attrs, ir_result_layouts):
      if layout is not None:
        attrs['mhlo.layout_mode'] = ir.StringAttr.get(layout)

  func_op.result_attrs = ir.ArrayAttr.get(
      [ir.DictAttr.get(attrs) for attrs in result_attrs])

  if arg_names:
    arg_locs: list[ir.Location] = [ir.Location.unknown()] * (
        num_dim_vars + num_tokens
    )
    for n in arg_names:
      arg_locs.append(ir.Location.name(n) if n else ir.Location.unknown())
    entry_block = func_op.add_entry_block(arg_locs)
  else:
    with ir.Location.unknown():
      entry_block = func_op.add_entry_block()

  # When lowering a function out of line, we do not include name context from
  # the caller. A function might have multiple callers, and it would be
  # incorrect to include any one caller's context. Exception: The main function
  # has no caller, so we include its name in the name stack.
  name_stack = (
      source_info_util.new_name_stack(name)
      if main_function
      else source_info_util.new_name_stack()
  )
  outer_traceback = (
      source_info_util.current().traceback if main_function else None
  )
  func_loc = source_info_to_location(ctx, None, name_stack, outer_traceback)
  with ir.InsertionPoint(entry_block), func_loc:
    flat_args = entry_block.arguments
    dim_var_values, _, const_arg_values, _ = util.split_list(
        flat_args, [num_dim_vars, num_tokens, num_const_args])
    const_args_and_avals = core.jaxpr_const_args(jaxpr.jaxpr)
    if num_const_args == 0:
      # If we did not hoist the constants out of this function, lower them now
      const_arg_values = [ir_constant(c, aval=aval)
                          for c, aval in const_args_and_avals]
    const_lowering: dict[tuple[int, core.AbstractValue], IrValues] = {
        (id(c), aval): c_arg
        for (c, aval), c_arg in zip(const_args_and_avals, const_arg_values)
    }

    # A lowering context just for function body entry/exit code.
    entry_lowering_ctx = LoweringRuleContext(
        module_context=ctx, name_stack=name_stack, traceback=None,
        primitive=None, avals_in=[], avals_out=None,
        tokens_in=TokenSet.create([]), tokens_out=None,
        axis_size_env=None, dim_var_values=dim_var_values,
        const_lowering=const_lowering)
    if not use_sharding_annotations and ir_arg_shardings is not None:
      flat_args = [
          a if s is None else wrap_with_sharding_op(entry_lowering_ctx, a, a_aval, s)
          for a, s, a_aval in zip(flat_args, ir_arg_shardings, input_avals)]

    if ir_arg_shardings is not None and main_function:
      flat_args = [
          replicate_trailing_dims(entry_lowering_ctx, o, a)
          if (a is not core.abstract_token and
              dtypes.issubdtype(a.dtype, dtypes.extended) and
              (s is None or all_unconstrained(rs, a))) else o
          for o, s, a, rs in zip(flat_args, ir_arg_shardings, input_avals,
                                 arg_shardings)  # pyrefly: ignore[bad-argument-type]  # pyrefly#2385
      ]

    unflattened_args = input_types_treedef.unflatten(flat_args)
    _, token_args, _, unflattened_args = util.split_list(
        unflattened_args,
        [num_dim_vars, num_tokens, num_const_args])
    tokens_in = TokenSet(dict(zip(effects, token_args)))
    args: list[IrValues] = unflattened_args
    unique_consts = {
        id(c): _ir_constant(c, aval=var.aval)
        for c, var in zip(jaxpr.consts, jaxpr.jaxpr.constvars)
    }
    consts_for_constvars = [unique_consts[id(c)] for c in jaxpr.consts]

    out_vals, tokens_out = jaxpr_subcomp(
        ctx, jaxpr.jaxpr, name_stack, tokens_in, consts_for_constvars, *args,
        dim_var_values=dim_var_values, const_lowering=const_lowering,
        outer_traceback=outer_traceback)
    outs: list[IrValues] = []
    for eff in effects:
      outs.append(tokens_out.get(eff))
    outs.extend(out_vals)

    flat_outputs, _ = ir_tree_registry.flatten(outs)

    if not use_sharding_annotations and ir_result_shardings is not None:
      flat_outputs = [
          o if s is None else wrap_with_sharding_op(entry_lowering_ctx, o, o_aval, s)
          for o, s, o_aval in zip(flat_outputs, ir_result_shardings, output_avals)]

    # Insert a custom call if output is on host because XLA needs that to do the
    # transfer.
    if custom_call_ir_result_memory_kinds is not None and main_function:
      flat_outputs = [
          o if mk is None else wrap_with_memory_kind(ctx, o, mk, o_aval)
          for o, mk, o_aval in zip(
              flat_outputs, custom_call_ir_result_memory_kinds, output_avals)]

    if ir_result_shardings is not None and main_function:
      flat_outputs = [
          replicate_trailing_dims(entry_lowering_ctx, o, a)
          if (a is not core.abstract_token and
              dtypes.issubdtype(a.dtype, dtypes.extended) and
              (s is None or all_unconstrained(rs, a))) else o
          for o, s, a, rs in zip(flat_outputs, ir_result_shardings, output_avals,
                                 result_shardings)  # pyrefly: ignore[bad-argument-type]  # pyrefly#2385
      ]

    func_dialect.return_(flat_outputs)

  return func_op

