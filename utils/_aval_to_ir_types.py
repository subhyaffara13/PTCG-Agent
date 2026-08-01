
def _aval_to_ir_types(ctx: ModuleContext, aval: core.AbstractValue) -> IrTypes:
  if (cached := ctx.aval_to_ir_types_cache.get(aval)) is not None:
    return cached
  try:
    res = ir_type_handlers[type(aval)](aval)
  except KeyError as err:
    raise TypeError(f"No ir_type_handler for aval type: {type(aval)}") from err
  ctx.aval_to_ir_types_cache[aval] = res
  return res

