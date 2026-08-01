
def _sort_lower(ctx, *operands, dimension, is_stable, num_keys):
  assert all(isinstance(x, core.ShapedArray) for x in ctx.avals_in), ctx.avals_in
  flat_out_types, _ = mlir.ir_tree_registry.flatten(
      map(partial(mlir.aval_to_ir_types, ctx.module_context), ctx.avals_out))
  flat_operands, _ = mlir.ir_tree_registry.flatten(operands)
  sort = hlo.SortOp(flat_out_types,
                    flat_operands,
                    dimension=mlir.i64_attr(dimension),
                    is_stable=ir.BoolAttr.get(is_stable))
  scalar_s = lambda a: a.sharding.update(spec=P())
  scalar_avals = [aval.update(shape=(), sharding=scalar_s(aval))
                  for aval in ctx.avals_in]
  scalar_types = safe_map(partial(mlir.aval_to_ir_type, ctx.module_context), scalar_avals)
  comparator = sort.comparator.blocks.append(
      *util.flatten(zip(scalar_types, scalar_types)))
  with ir.InsertionPoint(comparator):
    lower_comparator = mlir.lower_fun(partial(_sort_lt_comparator),
                                      multiple_results=False)
    sub_ctx = ctx.replace(primitive=None,
                          avals_in=util.flatten(zip(scalar_avals, scalar_avals)),
                          avals_out=[core.ShapedArray((), np.bool_)])

    out = lower_comparator(sub_ctx, *comparator.arguments, num_keys=num_keys)
    flat_out, _ = mlir.ir_tree_registry.flatten(out)
    hlo.return_(flat_out)
  return [mlir.lower_with_sharding_in_types(ctx, op, aval)
          for op, aval in zip(sort.results, ctx.avals_out)]

