
def _check_carry_same_references(carry_arg, carry_arg_out):
  def check_carry_same_references(key_path, arg, out):
    if (
      not isinstance(arg, jax.Array) or not isinstance(out, jax.Array)
    ) and arg is not out:
      raise ValueError(
        'Carry references must be the same between iterations. '
        f'Got {arg=} with id={id(arg)} and {out=} with id={id(out)} '
        f'at carry{jax.tree_util.keystr(key_path)}'
      )

  jax.tree_util.tree_map_with_path(
      check_carry_same_references,
      carry_arg,
      carry_arg_out,
      is_leaf=lambda x: graphlib.is_graph_node(x)
      and not isinstance(x, variablelib.Variable),
  )

