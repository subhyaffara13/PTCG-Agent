
def check_symbolic_scope_errors(fun_jax, args_specs, kwargs_specs):
  symbolic_scope: tuple[shape_poly.SymbolicScope, tree_util.KeyPath] | None = None
  for k_path, aval in tree_util.tree_flatten_with_path((args_specs, kwargs_specs))[0]:
    # Static args may have no `shape` attribute.
    if not hasattr(aval, "shape"):
      continue
    for d in aval.shape:
      if shape_poly.is_symbolic_dim(d):
        if symbolic_scope is None:
          symbolic_scope = (d.scope, k_path)
          continue
        symbolic_scope[0]._check_same_scope(
            d, when=f"when exporting {util.fun_name(fun_jax)}",
            self_descr=f"current (from {shape_poly.args_kwargs_path_to_str(symbolic_scope[1])}) ",
            other_descr=shape_poly.args_kwargs_path_to_str(k_path))

