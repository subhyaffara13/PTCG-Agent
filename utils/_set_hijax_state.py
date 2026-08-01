
def _set_hijax_state(hijax_var, variable: Variable):
  leaves, treedef = jax.tree.flatten(variable)
  set_variable_p.bind(
    hijax_var, *leaves, treedef=treedef, var_type=type(variable)
  )

