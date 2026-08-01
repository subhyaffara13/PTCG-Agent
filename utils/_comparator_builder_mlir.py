
def _comparator_builder_mlir(ctx, op_type, is_max_k):
  scalar = ir.RankedTensorType.get([], op_type)
  index = ir.RankedTensorType.get([], ir.IntegerType.get_signless(32))
  ir_types = [scalar, scalar, index, index]
  result_types = [ir.RankedTensorType.get([], ir.IntegerType.get_signless(1))]

  comparator_type = ir.FunctionType.get(ir_types, result_types)
  with ir.InsertionPoint.at_block_begin(ctx.module_context.module.body):
    comparator = func.FuncOp(
        "top_k_{}_{}_comparator".format('gt' if is_max_k else 'lt', op_type),
        comparator_type)
  ctx.module_context.symbol_table.insert(comparator)

  entry_block = comparator.add_entry_block()
  with ir.InsertionPoint(entry_block):
    p0, p1, _, _ = entry_block.arguments
    direction = hlo.ComparisonDirectionAttr.get('GT' if is_max_k else 'LT')
    cmp_result = hlo.compare(p0, p1, comparison_direction=direction)
    hlo.return_([cmp_result])

  return comparator

