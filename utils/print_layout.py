
def print_layout(format: _Union[str, _ods_ir.StringAttr], value: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> PrintLayoutOp:
  return PrintLayoutOp(format=format, value=value, loc=loc, ip=ip)


def print_layout(fmt: str, x: jax.typing.ArrayLike | _Ref) -> None:
  """Prints the layout chosen by Mosaic GPU for a given array or TMEM reference.

  This is evaluated at compile-time and has no incidence on the runtime behavior
  of the program.

  Args:
    fmt: The format string to use for printing the layout.
    x: The array or TMEM reference to print the layout of.
  """
  if isinstance(x, pallas_core.TransformedRef):
    transforms_leaves, transforms_tree = jax.tree.flatten(x.transforms)
    x = x.ref
  else:
    transforms_leaves, transforms_tree = [], None
  print_layout_p.bind(
      x,
      fmt=fmt,
      *transforms_leaves,
      transforms_tree=transforms_tree,
  )

