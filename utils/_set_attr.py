
def _set_attr(v: ir.Value, name: str, attr: ir.Attribute) -> None:
  if not isinstance(v, ir.BlockArgument):
    v.owner.attributes[name] = attr  # pyrefly: ignore[missing-attribute]
    return

  arg = ir.BlockArgument(v)
  name += f"_arg{arg.arg_number}"
  owner = arg.owner
  is_entry = owner.region.blocks[0] == owner
  if not is_entry:
    return
  if (op := owner.owner.operation) and not isinstance(op, tt_dialect.FuncOp):
    op.attributes[name] = attr

