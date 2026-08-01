
def solve_dim_vars(
    args_avals: Sequence[core.ShapedArray],
    args_kwargs_tree: tree_util.PyTreeDef,
    ) -> tuple[DimVarEnv, ShapeConstraints, Sequence[tuple[str, int, int]]]:
  """Solves dimension variables in a called function's avals in terms of actual argument shapes.

  For example, given:

     args_avals = [ShapedArray((3, a, a + b), f32)]

  we introduce fresh "synthetic" dimension variables to represent the actual
  dimension size of actual arguments for each non-constant dimension.
  Each synthetic variable has a name, an arg_idx, and a dim_idx, e.g.:

    synthetic_vars = [("args[0].shape[1]", 0, 1), ("args[0].shape[2]", 0, 2)]

  and then we express the solution for the unknown dimension variables {a, b}
  as symbolic expressions in terms of the synthetic variables:

    dict(a=args[0].shape[1], b=args[0].shape[2] - args[0].shape[1])

  Not all equations are solvable. For now, we solve first the linear
  uni-variate equations, then the solved variables are used to simplify the
  remaining equations to linear uni-variate equations, and the process
  continues until all dimension variables are solved.

  Args:
    args_avals: the abstract values of the `args`, with shapes that may
      include unknown dimension variables.
    args_kwargs_tree: a PyTreeDef that describes the tuple `(args, kwargs)`
      from which the flat sequence `args_avals` is extracted. Used for
      describing args and kwargs in synthetic variable names and in
      error messages.

  Returns: a 3-tuple with: (a) the solution for the unknown dimension variables
   (b) a list of constraints that must be satisfied for the solution to be a
   valid one, and (c) and the list of synthetic variables that may appear in
   the solution and the constraints.

  Raises ValueError if it cannot solve some dimension variable.
  """
  dim_equations: list[_DimEquation] = []
  synth_dimension_vars: list[tuple[str, int, int]] = []
  # tuples with argument name and its polymorphic shape ('args[0]', '(a, a + b'))
  polymorphic_shape_specs: list[tuple[str, str]] = []
  for arg_idx, aval in enumerate(args_avals):
    if all(not is_symbolic_dim(d) for d in aval.shape):
      continue
    polymorphic_shape_specs.append(
      (pretty_print_dimension_descriptor(args_kwargs_tree, arg_idx, None),
       str(aval.shape)))
    for dim_idx, aval_d in enumerate(aval.shape):
      if is_symbolic_dim(aval_d):
        synth_dim_var = pretty_print_dimension_descriptor(args_kwargs_tree,
                                                          arg_idx, dim_idx)
        synth_dimension_vars.append((synth_dim_var, arg_idx, dim_idx))
        dim_equations.append(
            _DimEquation(aval_dim_expr=aval_d,
                         dim_name=synth_dim_var))

  solution, shape_constraints = _solve_dim_equations(dim_equations,
                                                     polymorphic_shape_specs)
  return solution, shape_constraints, synth_dimension_vars

