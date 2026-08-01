
def len_ir_types(x: IrTypes) -> int:
  return 1 if isinstance(x, ir.Type) else len(x)

