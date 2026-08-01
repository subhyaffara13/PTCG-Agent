
def pp_var(v: Var | Literal, context: JaxprPpContext, *,
           print_literal_dtype: bool = True,
           is_binder: bool = False) -> pp.Doc:
  name = v.pretty_print(context, print_dtype=print_literal_dtype)
  if (isinstance(v, Var) and not isinstance(v, DropVar)):
    if is_binder:
      return pp.text(name, anchor=f"v_{name}")
    else:
      return pp.text(name, href=f"#v_{name}")
  return pp.text(name)

