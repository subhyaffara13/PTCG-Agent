
def compute_dim_vars_from_arg_shapes(
    args_avals: Sequence[core.ShapedArray],
    *actual_args: typing.Array,
    args_kwargs_tree: tree_util.PyTreeDef) -> Sequence[typing.Array]:
  """Computes values of dimension variables to unify args_avals with actual arguments.

  Like `solve_dim_vars` except that here we express the solution as
  JAX arrays that reference the `actual_args`. This function can be used to
  generate the code for computing the dimension variables. It also generates
  the shape assertions.

  Returns:
    The values of the dimension variables, in the order determined by
    `all_dim_vars(args_avals)`.
  """
  dim_vars = all_dim_vars(args_avals)
  solution, shape_constraints, synth_dim_vars = solve_dim_vars(
      tuple(args_avals), args_kwargs_tree=args_kwargs_tree)

  # Replace the synthetic vars with the dynamic shape of the actual arg
  synthetic_env: DimVarEnv = {
      vname: dimension_size_p.bind(actual_args[arg_idx], dimension=dim_idx)
      for (vname, arg_idx, dim_idx) in synth_dim_vars
  }
  synthetic_eval = ShapeEvaluator(synthetic_env)
  shape_constraints.shape_assertions(synthetic_eval)
  return tuple(synthetic_eval.evaluate(solution[var]) for var in dim_vars)

