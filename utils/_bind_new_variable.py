
def _bind_new_variable(
    *leaves, treedef, var_type, has_qdd, ref
) -> HijaxVariable:
  """Binds new_variable_p after instantiating any Zero tangents."""
  leaves = tuple(hjx.instantiate_zeros(leaf) for leaf in leaves)
  return new_variable_p.bind(
    *leaves,
    treedef=treedef,
    var_type=var_type,
    has_qdd=has_qdd,
    ref=ref,
  )

