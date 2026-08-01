
def _composite_lowering(
    ctx: mlir.LoweringRuleContext,
    *args: Any,
    name: str,
    attributes: Sequence[tuple[str, tuple[Any, ...], tree_util.PyTreeDef]],
    version: int,
    jaxpr: core.ClosedJaxpr,
):
  """Makes composite which calls the implementation function.

  Lowering a composite primitive to a ``stablehlo.composite`` op.

  Args:
    ctx: The MLIR context.
    *args: The arguments to the composite.
    name: The name of the composite.
    attributes: The attributes of the composite.
    version: The version of the composite.
    jaxpr: The jaxpr of the underlying composite.

  Returns:
    The results of the composite.
  """
  const_args_and_avals = core.jaxpr_const_args(jaxpr.jaxpr)
  const_args, const_avals = util.unzip2(const_args_and_avals)
  const_arg_values = tuple(
      mlir.ir_constants(c, const_lowering=ctx.const_lowering, aval=aval)
      for c, aval in const_args_and_avals
  )
  in_avals = (*const_avals, *ctx.avals_in)
  func_op, _, _ = mlir.lower_called_computation(
      name,
      jaxpr,
      ctx.module_context,
      len(const_args),
      in_avals,
      ctx.avals_out,
      ctx.tokens_in,
  )

  composite_attrs = {}
  for k, leaves, treedef in attributes:
    v = treedef.unflatten(leaves)
    if v is not None:
      composite_attrs[k] = mlir.ir_attribute(v)
  symbol_name = func_op.name.value
  flat_args, _ = mlir.ir_tree_registry.flatten(const_arg_values + args)
  return hlo.CompositeOp(
      func_op.type.results,
      flat_args,
      name=ir.StringAttr.get(name),
      decomposition=ir.FlatSymbolRefAttr.get(symbol_name),
      composite_attributes=ir.DictAttr.get(composite_attrs),
      version=mlir.i32_attr(version),
  ).results

