
def to_opt_state(tree):
  def _to_opt_state(x):
    if isinstance(x, Variable):
      opt_metadata = x.get_metadata()
      if 'optimizer_sharding' in opt_metadata:
        opt_metadata['out_sharding'] = opt_metadata.pop('optimizer_sharding')
      opt_state = OptVariable(x.get_value(), **opt_metadata)  # type: ignore
    else:
      opt_state = OptArray(x)
    return opt_state

  tree = jax.tree.map(
    _to_opt_state,
    tree,
    is_leaf=lambda x: isinstance(x, Variable),
  )
  return tree

