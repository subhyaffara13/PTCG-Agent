import functools

def lower_jaxpr_to_mosaic_gpu(
    module_ctx: ModuleContext,
    launch_ctx: mgpu.LaunchContext,
    jaxpr: jax_core.Jaxpr,
    args: Sequence[ir.Value],
    consts=(),
) -> Sequence[ir.Value]:
  env = {}

  def read_env(atom: jax_core.Atom):
    return atom.val if isinstance(atom, jax_core.Literal) else env[atom]

  def write_env(var: jax_core.Var, val, require_value: bool = True):
    env[var] = val
    # TODO(apaszke): Handle other avals (refs, etc.).
    if isinstance(aval := var.aval, jax_core.ShapedArray):
      # TODO(apaszke): Clarify the type invariants for lane semantics?
      if module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
        # Shaped arrays must be vectors if and only if their shape is non-empty.
        # Those with empty shapes should be represented by their scalar type.
        mlir_dtype = mgpu_utils.dtype_to_ir_type(aval.dtype)
        if not isinstance(val, ir.Value):
          if require_value:
            raise AssertionError(f"Shaped arrays must be represented by ir.Values, got: {val}")
          else:
            if aval.shape:
              raise AssertionError("Only scalars can be represented by non-ir.Values")
            return  # Skip following checks.
        if aval.shape:
          if not isinstance(val.type, ir.VectorType):
            raise AssertionError(f"Non-scalar arrays must be represented by vectors, got: {val.type}")
          vty = ir.VectorType(val.type)
          if vty.element_type != mlir_dtype:
            raise AssertionError(f"Vector element type must match ShapedArray dtype, got: {val.type} != {mlir_dtype}")
          if tuple(vty.shape) != aval.shape:
            raise AssertionError(f"Vector shape must match ShapedArray shape, got: {vty.shape} != {aval.shape}")
        else:
          if isinstance(val.type, ir.VectorType):
            raise AssertionError(f"Scalars must be represented by non-vector types, got: {val.type}")
          if val.type != mlir_dtype:
            raise AssertionError(f"Scalar type must match ShapedArray dtype, got: {val.type} != {mlir_dtype}")

  foreach(
      functools.partial(write_env, require_value=False), jaxpr.constvars, consts
  )
  foreach(functools.partial(write_env, require_value=False), jaxpr.invars, args)

  # TODO(justinfu): Handle transform scopes.
  last_local_name_stack: list[str] = []
  named_regions = []
  for i, eqn in enumerate(jaxpr.eqns):
    invals = map(read_env, eqn.invars)
    eqn_name_stack = module_ctx.name_stack + eqn.source_info.name_stack
    loc = mlir.source_info_to_location(
        module_ctx,
        eqn.primitive,
        eqn_name_stack,
        eqn.source_info.traceback or module_ctx.outer_traceback,
    )
    with source_info_util.user_context(eqn.source_info.traceback), loc:
      if eqn.primitive not in mosaic_lowering_rules[
          (module_ctx.lowering_semantics, module_ctx.primitive_semantics)]:
        raise NotImplementedError(
            "Unimplemented primitive in Pallas Mosaic GPU lowering:"
            f" {eqn.primitive.name} for lowering semantics"
            f" {module_ctx.lowering_semantics} and user thread semantics"
            f" {module_ctx.primitive_semantics}. Please file an issue at"
            " https://github.com/jax-ml/jax/issues/new/choose."
        )
      new_local_name_stack = [scope.name for scope in eqn.source_info.name_stack.stack]
      popped, pushed = _compute_name_stack_updates(last_local_name_stack, new_local_name_stack)
      last_local_name_stack = new_local_name_stack
      for _ in popped:
        named_regions.pop().close()
      for name in pushed:
        wrapper_stack = contextlib.ExitStack()
        wrapper_stack.enter_context(launch_ctx.named_region(name))
        named_regions.append(wrapper_stack)
      rule = mosaic_lowering_rules[
          (module_ctx.lowering_semantics, module_ctx.primitive_semantics)
          ][eqn.primitive]
      # If the equation is immediately followed by a layout cast on its output,
      # we provide the layout as a hint to the rule.
      out_layout_hint = None
      if i + 1 < len(jaxpr.eqns):
        lookahead_eqn = jaxpr.eqns[i + 1]
        is_layout_cast = lookahead_eqn.primitive == gpu_core.layout_cast_p
        uses_eqn_output = lookahead_eqn.invars == eqn.outvars
        if is_layout_cast and uses_eqn_output:
          out_layout_hint = lookahead_eqn.params["new_layout"].to_mgpu()
      rule_ctx = LoweringRuleContext(
          module_ctx,
          launch_ctx,
          avals_in=[cast(ShapedAbstractValue, v.aval) for v in eqn.invars],
          avals_out=[cast(ShapedAbstractValue, v.aval) for v in eqn.outvars],
          prim=eqn.primitive,
          out_layout_hint=out_layout_hint,
      )
      try:
        outvals = rule(rule_ctx, *invals, **eqn.params)
      except LoweringError:
        raise  # We only add the extra info to the innermost exception.
      except Exception as e:
        if not config.jax_pallas_verbose_errors.value:
          raise
        inval_types = map(lambda t: getattr(t, "type", None), invals)
        raise LoweringError(
            f"Exception while lowering eqn:\n  {eqn}\nWith context:\n "
            f" {rule_ctx}\nWith inval types={inval_types}\nIn jaxpr:\n{jaxpr}"
        ) from e
      if eqn.primitive.multiple_results:
        foreach(write_env, eqn.outvars, outvals)
      else:
        write_env(eqn.outvars[0], outvals)
  while named_regions:  # Drain the name stack.
    named_regions.pop().close()
  return map(read_env, jaxpr.outvars)

