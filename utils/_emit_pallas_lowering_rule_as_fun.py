
def _emit_pallas_lowering_rule_as_fun(
    ctx: LoweringContext,
    primitive: jax_core.Primitive,
    rule: Callable,
    rule_context: LoweringRuleContext,
    invals: Sequence[ir.Value],
    **params,
) -> func.FuncOp:
  """Emits the contents of a Pallas lowering rule as a detached function."""

  input_types = []
  user_grid_indices = (
      ctx.user_grid_indices
      if primitive in _primitives_needing_grid
      else None
  )
  if user_grid_indices is not None:
    input_types.extend(val.type for val in user_grid_indices)
  input_types.extend(val.type for val in invals)

  output_types = map(rule_context.aval_to_ir_type, rule_context.avals_out)

  func_name = f"_pallas_{primitive.name}"

  def body_builder(block_args: list[ir.Value]) -> list[ir.Value]:
    if user_grid_indices is not None:
      grid_arity = len(user_grid_indices)
      rule_args = block_args[grid_arity:]
      sub_ctx = rule_context.replace(
          lowering_context=ctx.replace(
              user_grid_indices=block_args[:grid_arity],
          )
      )
    else:
      sub_ctx = rule_context.replace(
          lowering_context=ctx.replace(
              user_grid_indices=None,
          )
      )
      rule_args = block_args

    outs = rule(sub_ctx, *rule_args, **params)

    flat_outs = list(outs) if primitive.multiple_results else [outs]
    flat_outs = [_ensure_mlir_value(x, aval)
                 for x, aval in zip(flat_outs, rule_context.avals_out)]

    if any(not isinstance(x, ir.Value) for x in flat_outs):
      # TODO(phawkins): this is probably from KeyScalarBundle primarily. Handle
      # this case and remove the exception.
      raise UncacheablePrimitiveError("Lowering rule returned non-ir.Value")
    return flat_outs

  return _emit_detached_func(func_name, input_types, output_types, body_builder)

