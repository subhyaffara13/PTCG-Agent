
def _move_scf_block_to_block_with_flattened_arguments(
    ctx: LoweringContext,
    old_block: ir.Block,
    new_block: ir.Block,
    last_op_type: type[ir.OpView],
    args_template: Sequence[_VectorTemplate | None],
    *new_leading_args: ir.Value,
) -> Sequence[_VectorTemplate | None]:
  """Moves the operations from `old_block` to `new_block`.

  The input arguments to the block, if any, are flattened using the provided
  `args_template`, except for any new_leading_args which are simply prepended
  to the flattened arguments and must be part of the template.

  The last operation of the old block must be of type `last_op_type` which
  is expected to be either a `scf.YieldOp` or a `scf.ConditionOp`. This
  operation is recreated with flattened output arguments.
  """
  out_template = None
  with ir.InsertionPoint(new_block):
    new_carry = _unflatten_ir_values(new_block.arguments[len(new_leading_args):], args_template)
    new_args = new_leading_args + tuple(new_carry)
    for old_arg, new_arg in zip(old_block.arguments, new_args, strict=True):
      old_arg.replace_all_uses_with(new_arg)
    for op in [*old_block]:
      if not isinstance(op, last_op_type):
        # `append` moves the operation.
        new_block.append(op)
        ctx.lower_op(op)
      else:
        assert out_template is None
        layouts = (
            inference_utils.in_layouts(op)
            if inference_utils.has_in_layouts_set(op)
            else []
        )
        if isinstance(op, scf.YieldOp):
          flat_operands, out_template = _flatten_ir_values(op.operands, layouts)
          scf.yield_(flat_operands)
        elif isinstance(op, scf.ConditionOp):
          flat_carry, out_template = _flatten_ir_values(op.args, layouts)
          scf.condition(op.condition, flat_carry)
        else:
          raise NotImplementedError(f"Unsupported op type: {op}")
        op.erase()
  assert out_template is not None
  return out_template

