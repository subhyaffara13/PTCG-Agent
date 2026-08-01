
def _to_abstract_variable(hijax_var: HijaxVariable):
  if hijax_var.has_qdd:
    treedef = None
    leaves = None
  else:
    leaves = tuple(map(jax.typeof, hijax_var._leaves))
    treedef = hijax_var._treedef
  return AbstractVariable(
    hijax_var._var_type,
    treedef,
    leaves,
    hijax_var.has_qdd,
    ref=hijax_var.ref,
  )

