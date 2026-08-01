
def jaxpr_subcomp(
    ctx: ModuleContext,
    jaxpr: core.Jaxpr,
    name_stack: source_info_util.NameStack,
    tokens: TokenSet,
    consts_for_constvars: Sequence[IrValues],
    *args: IrValues,
    dim_var_values: Sequence[ir.Value],
    const_lowering: dict[tuple[int, core.AbstractValue], IrValues],
    outer_traceback: xc.Traceback | None,
) -> tuple[Sequence[IrValues], TokenSet]:
  """Lowers a jaxpr into MLIR, inlined into an existing function.

  Assumes that an MLIR context, location, and insertion point are set.

  consts_for_constvars: the constants corresponding to jaxpr.constvars.
  dim_var_values: the list of dimension variables values in the current
    IR function, in the order of ctx.shape_poly_state.dim_vars.
  const_lowering: the lowering for constants, by constant id.
    See https://docs.jax.dev/en/latest/internals/constants.html
  """
  assert "gpu" not in ctx.platforms

  def read(v: core.Atom) -> IrValues:
    if type(v) is core.Literal:
      return _ir_constant(v.val, const_lowering=const_lowering, aval=v.aval)
    else:
      assert isinstance(v, core.Var)
      return env[v]

  def write(v: core.Var, node: IrValues):
    assert node is not None
    w: IrValues
    if isinstance(node, ir.Value):
      w = node
    else:
      if len(node) == 1:
        warnings.warn(
            "JAX lowering rules should not wrap singleton values in tuples. "
            "It will be an error to wrap a singleton value in a tuple in a "
            "future version of JAX.",
            DeprecationWarning, stacklevel=2)
        w = node[0]
      else:
        w = tuple(node)
    env[v] = w

  env: dict[core.Var, IrValues] = {}

  assert all(_is_ir_values(v) for v in args), args
  assert all(_is_ir_values(v) for v in consts_for_constvars), \
    consts_for_constvars
  assert isinstance(name_stack, source_info_util.NameStack), type(name_stack)
  assert len(args) == len(jaxpr.invars), (jaxpr, args)
  assert len(consts_for_constvars) == len(jaxpr.constvars), \
    (jaxpr, consts_for_constvars)
  assert len(ctx.shape_poly_state.dim_vars) == len(dim_var_values), \
    (ctx.shape_poly_state.dim_vars, dim_var_values)
  foreach(write, jaxpr.constvars, consts_for_constvars)
  foreach(write, jaxpr.invars, args)
  outer_traceback = outer_traceback or xc.Traceback()
  should_log_constants = (config.use_simplified_jaxpr_constants.value and
                          config.captured_constants_warn_bytes.value >= 0)
  for eqn in jaxpr.eqns:
    if should_log_constants:
      for v in eqn.invars:
        if type(v) is core.Literal and core.is_hoistable(v):
          log_closed_over_constant(v, eqn, jaxpr._debug_info)

    in_nodes = tuple(map(read, eqn.invars))

    eqn_name_stack = name_stack + eqn.source_info.name_stack
    traceback = (eqn.source_info.traceback or xc.Traceback()) + outer_traceback

    can_cache_lowering = (eqn.primitive not in _uncacheable_primitives)
    avals_in = tuple(v.aval for v in eqn.invars)

    if can_cache_lowering:
      cache_key = LoweringCacheKey(
          primitive=eqn.primitive,
          eqn_ctx=eqn.ctx,
          avals_in=avals_in,
          effects=frozenset(eqn.effects),
          params=tuple(sorted(eqn.params.items())),
          platforms=tuple(ctx.platforms),
      )
      cache_entry = ctx.lowering_cache.get(cache_key, None)
      loc = source_info_to_location(ctx, None, eqn_name_stack, traceback)
      with loc:
        if cache_entry is None:
          assert cache_key is not None
          cache_entry = _cached_lowering_miss(
              ctx, eqn, cache_key, avals_in, **eqn.params
          )
        out_nodes, tokens_out = _emit_cached_call(
            ctx, eqn, tokens, tuple(dim_var_values), const_lowering,
            cache_entry, *in_nodes
        )
    else:
      # If we cannot cache the lowering, lower inline.
      loc = source_info_to_location(ctx, eqn.primitive, eqn_name_stack, traceback)
      with (source_info_util.user_context(eqn.source_info.traceback), loc,
            eqn.ctx.manager):
        axis_size_env = None
        rule_ctx = LoweringRuleContext(
            module_context=ctx, primitive=eqn.primitive,
            name_stack=eqn_name_stack,
            traceback=traceback,
            avals_in=avals_in,
            avals_out=tuple(v.aval for v in eqn.outvars), tokens_in=tokens,
            tokens_out=None, jaxpr_eqn_ctx=eqn.ctx,
            dim_var_values=dim_var_values,
            axis_size_env=axis_size_env,
            const_lowering=const_lowering)
        platform_rules, default_rule, _ = _get_lowering_rules(
            ctx, eqn.primitive, eqn.ctx)
        out_nodes = _uncached_lowering(
            eqn.primitive, eqn.ctx, eqn.effects, platform_rules, default_rule,
            rule_ctx, *in_nodes,
            **eqn.params)
        tokens_out = rule_ctx.tokens_out

    if tokens_out is not None:
      tokens = tokens_out

    foreach(write, eqn.outvars, out_nodes)
  return tuple(read(v) for v in jaxpr.outvars), tokens


def jaxpr_subcomp(
    ctx: LoweringContext, jaxpr: jax_core.Jaxpr, *args: ir.Value
) -> list[ir.Value]:
  assert not jaxpr.constvars
  env = {}
  block_shape_env = {}

  def read_block_shape(atom: jax_core.Atom):
    if isinstance(atom, jax_core.Literal):
      return None
    # Not all refs may have block shapes (e.g. those introduced with
    # `jax.empty_ref`), but lowering expects them to exist---so we just return
    # the shape of the ref in this case.
    if atom not in block_shape_env and isinstance(atom.aval, state.AbstractRef):
      return atom.aval.shape
    return block_shape_env.get(atom, None)

  def read_env(atom: jax_core.Atom):
    return atom.val if isinstance(atom, jax_core.Literal) else env[atom]

  def write_env(var: jax_core.Var, val):
    is_valid_type = isinstance(val, (ir.Value, KeyScalarBundle))
    assert is_valid_type, type(val)
    env[var] = val

  for invar, bs in zip(jaxpr.invars, ctx.block_shapes):
    block_shape_env[invar] = bs
  foreach(write_env, jaxpr.invars, args)

  initial_name_stack = [scope.name for scope in ctx.name_stack.stack]
  current_name_stack: list[str] = []
  # TODO(justinfu): Handle transform scopes.
  current_name_stack.extend(initial_name_stack)
  for eqn in jaxpr.eqns:
    invals = map(read_env, eqn.invars)
    eqn_name_stack = ctx.name_stack + eqn.source_info.name_stack
    loc = mlir.source_info_to_location(
        ctx, eqn.primitive, eqn_name_stack, eqn.source_info.traceback
    )
    with (source_info_util.user_context(eqn.source_info.traceback), loc,
          eqn.ctx.manager):
      if eqn.primitive in lowering_rules[ctx.kernel_type]:
        if (eqn.primitive, ctx.kernel_type) not in skip_mlir_conversions:
          invals = [
              _ensure_mlir_value(x, cast(ShapedAbstractValue, v.aval))
              for x, v in zip(invals, eqn.invars)
          ]
        avals_in = cast(tuple[ShapedAbstractValue, ...],
                        tuple(v.aval for v in eqn.invars))
        avals_out = cast(tuple[ShapedAbstractValue, ...],
                         tuple(v.aval for v in eqn.outvars))
        block_shapes = tuple(read_block_shape(x) for x in eqn.invars)

        # Insert trace_start and trace_stop ops on named_scope boundaries.
        name_stack = [scope.name for scope in eqn_name_stack.stack]
        popped, pushed = _compute_name_stack_updates(
            current_name_stack, name_stack)
        current_name_stack = name_stack
        for _ in popped:
          tpu.trace_stop()
        for name in pushed:
          tpu.trace_start(message=name, level=10)

        cache_entry = None
        cache_key = None
        rule_context = None

        # TODO(phawkins): allow KeyScalarBundle here as well as ir.Value.
        can_cache = (eqn.primitive not in _uncacheable_primitives and
                     all(isinstance(x, ir.Value) for x in invals))
        if can_cache:
          grid_arity = (
              len(ctx.user_grid_indices)
              if (eqn.primitive in _primitives_needing_grid and ctx.user_grid_indices is not None)
              else 0
          )
          cache_key = PallasLoweringCacheKey(
              primitive=eqn.primitive,
              kernel_type=ctx.kernel_type,
              avals_in=avals_in,
              avals_out=avals_out,
              params=tuple(sorted(eqn.params.items())),
              block_shapes=block_shapes,
              grid_arity=grid_arity,
              forward_compatible=ctx.forward_compatible,
              fuse_transposed_lhs_in_matmul=ctx.fuse_transposed_lhs_in_matmul,
              grid_sizes=ctx.grid_sizes,
              vmapped_dims=ctx.vmapped_dims,
              dynamic_shape_env=(
                  ctx.dynamic_shape_env.snapshot()
                  if ctx.dynamic_shape_env is not None
                  else None
              ),
          )
          cache_entry = ctx.lowering_cache.get(cache_key, None)

        if cache_entry is None:
          rule_context = LoweringRuleContext(
              ctx,
              cast(Sequence[ShapedAbstractValue], avals_in),
              cast(Sequence[ShapedAbstractValue], avals_out),
              block_shapes,
          )
          if cache_key is not None:
            try:
              cache_entry = _emit_pallas_lowering_rule_as_fun(
                  ctx, eqn.primitive,
                  lowering_rules[ctx.kernel_type][eqn.primitive],
                  rule_context, invals, **eqn.params
              )
              if ctx.dynamic_shape_env is not None:
                cache_key = dataclasses.replace(
                    cache_key,
                    dynamic_shape_env=ctx.dynamic_shape_env.snapshot(),
                )
              ctx.lowering_cache[cache_key] = cache_entry
            except UncacheablePrimitiveError:
              pass

        if cache_entry is not None:
          call_args = []
          if eqn.primitive in _primitives_needing_grid and ctx.user_grid_indices is not None:
            call_args.extend(ctx.user_grid_indices)
          call_args.extend(invals)
          outs = jax_mlir_ext.inlined_func_call(
            cache_entry.operation, call_args)

          ans = outs if eqn.primitive.multiple_results else outs[0]
        else:
          try:
            assert rule_context is not None
            ans = lowering_rules[ctx.kernel_type][eqn.primitive](
                rule_context, *invals, **eqn.params
            )
          except LoweringException:
            raise  # We only add the extra info to the innermost exception.
          except Exception as e:
            if not config.jax_pallas_verbose_errors.value:
              raise
            msg = (f"{type(e).__name__}: {e}\n" +
                  "Additional diagnostics: \n" +
                  f"Failing jaxpr equation: {eqn}\n")
            new_error = LoweringException(msg)
            # We insert the traceback here so that the user code shows
            # up in the traceback for the post-transform error.
            if eqn.source_info.traceback is not None:
              tb = eqn.source_info.traceback.as_python_traceback()
              new_error.__traceback__ = traceback_util.filter_traceback(tb)
            raise new_error from e
      else:
        raise NotImplementedError(
            "Unimplemented primitive in Pallas TPU lowering for"
            f" {ctx.kernel_type}: {eqn.primitive.name}. Please file an issue at"
            " https://github.com/jax-ml/jax/issues/new/choose."
        )
      if eqn.primitive.multiple_results:
        foreach(write_env, eqn.outvars, cast(Any, ans))
      else:
        write_env(eqn.outvars[0], ans)

  # Drain the name stack at the end of a jaxpr and insert trace_stop ops.
  popped, pushed = _compute_name_stack_updates(
      current_name_stack, initial_name_stack)
  for _ in popped:
    tpu.trace_stop()
  assert len(pushed) == 0

  outvals = map(read_env, jaxpr.outvars)
  outvals = [
      ir_constant(x) if isinstance(var, jax_core.Literal) else x
      for x, var in zip(outvals, jaxpr.outvars)
  ]
  return outvals

