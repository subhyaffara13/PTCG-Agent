
def check_same_variables(inputs, outputs, transform_name: str = ''):
  def _check(in_leaf, out_leaf):
    if isinstance(in_leaf, variablelib.Variable) and in_leaf is not out_leaf:
      raise ValueError(
        f'{transform_name} Variable identity must be preserved '
        'across iterations.'
      )
  is_leaf = lambda x: isinstance(x, (Mask, variablelib.Variable))
  jax.tree.map(
    _check, inputs, outputs,
    is_leaf=is_leaf,
  )

