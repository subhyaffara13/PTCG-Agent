
def _new_hijax_from_variable(variable: Variable) -> HijaxVariable:
  has_qdd = not variable.ref
  leaves, treedef = jax.tree.flatten(variable)
  var_type = type(variable)
  hijax_var = _bind_new_variable(
    *leaves,
    treedef=treedef,
    var_type=var_type,
    has_qdd=has_qdd,
    ref=variable.ref,
  )
  return hijax_var

