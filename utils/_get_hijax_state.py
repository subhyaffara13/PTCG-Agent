
def _get_hijax_state(hijax_var: HijaxVariable | AbstractVariable) -> Variable:
  if hijax_var.has_qdd:
    tys: VariableQDD = jax.experimental.cur_qdd(hijax_var)
    leaf_vals = get_variable_p.bind(
      hijax_var,
      treedef=tys.treedef,
      avals=tuple(tys.leaf_avals),
      var_type=hijax_var._var_type,
      has_qdd=hijax_var.has_qdd,
    )
    variable = jax.tree.unflatten(tys.treedef, leaf_vals)
  else:
    assert hijax_var._treedef is not None
    assert hijax_var._leaves is not None
    if isinstance(hijax_var, (jax.core.Tracer, AbstractVariable)):
      leaf_avals = hijax_var._leaves
    else:
      leaf_avals = tuple(map(jax.typeof, hijax_var._leaves))
    leaf_vals = get_variable_p.bind(
      hijax_var,
      treedef=hijax_var._treedef,
      avals=leaf_avals,
      var_type=hijax_var._var_type,
      has_qdd=hijax_var.has_qdd,
    )
    variable = jax.tree.unflatten(hijax_var._treedef, leaf_vals)

  return variable

