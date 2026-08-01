
def attr_get(x):
  if isinstance(x, str):
    return ir.StringAttr.get(x)
  else:
    raise NotImplementedError(f'mlir attr handler for {type(x)=}')

