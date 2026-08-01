
def update_carry_variables(init_val, val_out):
  def _update(in_leaf, out_leaf):
    if isinstance(in_leaf, variablelib.Variable):
      in_leaf.update_from_state(out_leaf)
      return in_leaf
    return out_leaf

  return jax.tree.map(
    _update, init_val, val_out,
    is_leaf=lambda x: isinstance(x, variablelib.Variable),
  )

