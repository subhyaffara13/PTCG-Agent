from typing import Any

def lower_per_platform(ctx: LoweringRuleContext,
                       description: str,
                       platform_rules: dict[str, LoweringRule],
                       default_rule: LoweringRule | None,
                       effects: effects_lib.Effects,
                       *rule_args: ir.Value | tuple[ir.Value, ...],
                       **rule_kwargs) -> Sequence[ir.Value]:
  """Emits code for a primitive for the current lowering platform(s).

  For example, given
      platform_rules = dict(tpu=rule0, cpu=rule0)
      default_rule = rule1

  and
      ctx.module_context.lowering_parameters.platforms = ("cpu",)

  emits:
      rule0(ctx, *rule_args, **rule_kwargs)

  In case of multi-platform lowering, e.g., if
      ctx.module_context.lowering_parameters.platforms = ("cpu", "cuda", "tpu")

  emits:
    rule_idx = case current_platform_idx:
                   0: return 0  # cpu rule index
                   1: return 1  # cuda rule index
                   2: return 0  # tpu rule index
    output = case rule_idx
               0: return rule0(*rule_args, **rule_kwargs)
               1: return rule1(*rule_args, **rule_kwargs)

  Args:
   ctx: lowering context.
   description: a string to include in error messages.
   platform_rules: map platform names, e.g., "cpu", "cuda", to
     `LoweringRule`s, for the platforms that have non-default lowering.
   default_rule: an optional rule to use for platforms not in `platform_rules`.
   effects: the set of effects for the current primitive.
   rule_args: the args of the lowering rules.
   rule_kwargs: the kwargs of the lowering rules.
  """
  platforms: Sequence[str] = _platforms_for_eqn(ctx)
  # Special case the common case (single-platform lowering)
  if len(platforms) == 1:
    rule = platform_rules.get(platforms[0], default_rule)
    if rule is None:
      raise NotImplementedError(
        f"MLIR translation rule for primitive '{description}' not "
        f"found for platform {platforms[0]}")

  # Multi-platform lowering
  kept_rules: list[LoweringRule] = []  # Only the rules for the platforms of interest
  platform_to_kept_rules_idx: dict[str, int] = {}
  for p, prule in platform_rules.items():
    if p not in platforms:
      continue
    platform_to_kept_rules_idx[p] = len(kept_rules)
    kept_rules.append(prule)

  platforms_without_specific_rule = [p for p in platforms
                                     if p not in platform_to_kept_rules_idx]
  if platforms_without_specific_rule:
    if default_rule is None:
      raise NotImplementedError(
        f"MLIR translation rule for primitive '{description}' not "
        f"found for platforms {platforms_without_specific_rule}")
    for p in platforms_without_specific_rule:
      platform_to_kept_rules_idx[p] = len(kept_rules)
    kept_rules.append(default_rule)

  assert kept_rules
  # If there is a single rule left just apply the rule, without conditionals.
  if len(kept_rules) == 1:
    rule, = kept_rules
    output = type_cast(Sequence[IrValues], rule(ctx, *rule_args, **rule_kwargs))
    flat_output, _ = ir_tree_registry.flatten(output)
    for o, a in zip(flat_output, ctx.avals_out):
      if not isinstance(o, ir.BlockArgument):
        check_unreduced_constraint(o, a)
        wrap_compute_type_in_place(ctx, o)
        wrap_xla_metadata_in_place(ctx, o)
    return flat_output

  assert len(platforms) > 1 and len(kept_rules) >= 2, (platforms, kept_rules)
  assert len(ctx.dim_var_values) >= 1, "Must have a platform_index variable"

  # The first dim_var_values is the platform index
  current_platform_idx = ctx.dim_var_values[0]
  # Compute the rule index based on the current platform
  i32_type = aval_to_ir_type(ctx.module_context, core.ShapedArray((), dtype=np.int32))
  if current_platform_idx.type != i32_type:
    current_platform_idx = hlo.convert(i32_type, current_platform_idx)
  rule_idx_op = hlo.CaseOp([i32_type],
                           index=current_platform_idx,
                           num_branches=len(platforms))
  for i, p in enumerate(platforms):
    branch = rule_idx_op.regions[i].blocks.append()
    with ir.InsertionPoint(branch):
      hlo.return_([ir_constant(np.int32(platform_to_kept_rules_idx[p]))])
  ordered_effects = effects_lib.ordered_effects.filter_in(effects)
  rule_out_avals = [core.abstract_token] * len(ordered_effects) + ctx.avals_out
  output_types = [_aval_to_ir_types(ctx.module_context, a) for a in rule_out_avals]
  flat_output_types, output_types_treedef = ir_tree_registry.flatten(output_types)
  case_op = hlo.CaseOp(flat_output_types,
                      index=rule_idx_op.result,
                      num_branches=len(kept_rules))
  for i, rule in enumerate(kept_rules):
    platforms_for_rule = [p for p, rule_idx in platform_to_kept_rules_idx.items()
                          if rule_idx == i]
    inner_ctx = ctx.replace(platforms=platforms_for_rule)
    branch = case_op.regions[i].blocks.append()
    with ir.InsertionPoint(branch):
      output = type_cast(
          Sequence[IrValues], rule(inner_ctx, *rule_args, **rule_kwargs)
      )
      try:
        out_nodes, _ = ir_tree_registry.flatten(output)
      except TypeError as e:
        raise ValueError("Output of translation rule must be iterable: "
                        f"{description}, got output {output}") from e
      for o, a in zip(out_nodes, ctx.avals_out):
        if not isinstance(o, ir.BlockArgument):
          check_unreduced_constraint(o, a)
          wrap_compute_type_in_place(ctx, o)
          wrap_xla_metadata_in_place(ctx, o)
      if inner_ctx.tokens_out is not None:
        assert len(ordered_effects) == len(inner_ctx.tokens_out)
        out_nodes = [inner_ctx.tokens_out.get(eff)
                     for eff in ordered_effects] + out_nodes
      hlo.return_(out_nodes)

  results: Any = case_op.results
  if ordered_effects:
    unflattened_results = output_types_treedef.unflatten(results)
    tokens, results = util.split_list(
      unflattened_results,
      [len(ordered_effects)])
    tokens_out = ctx.tokens_in.update_tokens(
        TokenSet(dict(zip(ordered_effects, tokens))))
    ctx.set_tokens_out(tokens_out)
  return results

