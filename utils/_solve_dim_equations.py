
def _solve_dim_equations(
    eqns: list[_DimEquation],
    polymorphic_shape_specs: Sequence[tuple[str, str]]
) -> tuple[DimVarEnv, ShapeConstraints]:
  # Returns a shape environment and the shape constraints if it can solve all
  # dimension variables. Raises an exception if it cannot.
  shape_env: DimVarEnv = {}
  solution_error_message_pieces: list[str | DimSize] = [
    " Obtained dimension variables: "
  ]  # Error message describing the solution
  # Prepare error message piece describing the polymorphic shape specs
  poly_specs_err_msg = (
    " Using the following polymorphic shapes specifications: " +
    ",".join(f"{arg_name}.shape = {arg_spec}"
             for arg_name, arg_spec in polymorphic_shape_specs)) + "."
  solution_err_msg_trailer_errors = ". Please see https://docs.jax.dev/en/latest/export/shape_poly.html#shape-assertion-errors for more details."

  shape_constraints = ShapeConstraints()  # accumulate shape constraints
  scope: SymbolicScope | None = None

  def process_one_eqn(eqn: _DimEquation) -> bool:
    # We start with a DimEquation of the form `dim_expr = dim_value`
    # Try to rewrite the equation as `var * factor_var = dim_value_2` (a linear
    # uni-variate equation). Returns `False` if this rewrite fails.
    # Otherwise, compute the `var` value as `dim_value_2 // factor`, add it to
    # `shape_env` and return `True`.
    #
    # Invariant:
    #     var * factor_var + remaining_terms_from_dim_expr = dim_value
    var, var_k = None, None
    nonlocal scope
    if scope is None:
      scope = eqn.aval_dim_expr.scope
    elif config.enable_checks.value:
      scope._check_same_scope(eqn.aval_dim_expr, when=f"solving equation {eqn}")

    dim_value = _DimExpr._from_var(eqn.dim_name, scope)

    for term, term_k in eqn.aval_dim_expr._sorted_terms:
      # Perhaps we can already evaluate this term (all vars solved)
      try:
        term_value = term.evaluate(shape_env, scope)
      except UnexpectedDimVar:
        # `mon` still uses some variables not yet solved. We handle only the
        # case when `mon` is a single variable.
        v = term.to_var()
        if v is not None and var is None:
          var, var_k = v, term_k
          continue
      else:
        dim_value = dim_value + core.dim_constant(-1) * _evaluate_multiply(term_value, core.dim_constant(term_k))
        continue
      return False  # This equation cannot yet be used to solve a variable

    if var is not None:
      assert var_k is not None
      if var_k == 1:
        var_value = dim_value
      else:
        var_value, var_remainder = divmod(dim_value, core.dim_constant(var_k))
        shape_constraints.add_constraint(
            Comparator.EQ, var_remainder, 0,
            error_message_pieces=([
                "Input shapes do not match the polymorphic shapes specification. "
                "Division had remainder ", var_remainder,
                f" when computing the value of '{var}'." + poly_specs_err_msg
              ] + solution_error_message_pieces + [
                solution_err_msg_trailer_errors]))

      if not isinstance(var_value, _DimExpr):
        assert var_value.dtype == core.dim_value_dtype()  # pyrefly: ignore[missing-attribute]
      shape_env[var] = var_value  # pyrefly: ignore[unsupported-operation]
      solution_error_message_pieces.extend([
        f"'{var}' = ", var_value,
        f" from specification '{eqn.aval_dim_expr}' "
        f"for dimension {eqn.dim_name} (= ",
        _DimExpr._from_var(eqn.dim_name, eqn.aval_dim_expr.scope),
        "), "])

      shape_constraints.add_constraint(
          Comparator.GEQ, var_value, 1,
          error_message_pieces=[
                "Input shapes do not match the polymorphic shapes specification. "
                f"Expected value >= 1 for dimension variable '{var}'." +
                poly_specs_err_msg
              ] + solution_error_message_pieces + [
              solution_err_msg_trailer_errors])

      return True
    else:
      # All variables are resolved for this equation, we emit an assertion
      shape_constraints.add_constraint(
          Comparator.EQ,
          _DimExpr._from_var(eqn.dim_name, eqn.aval_dim_expr.scope),
          eqn.aval_dim_expr._evaluate(shape_env),
          error_message_pieces=([
            "Input shapes do not match the polymorphic shapes specification. "
            f"Found inconsistency between dimension size {eqn.dim_name} (= ",
            _DimExpr._from_var(eqn.dim_name, eqn.aval_dim_expr.scope),
            f") and the specification '{eqn.aval_dim_expr}' (= ",
            eqn.aval_dim_expr._evaluate(shape_env),
            ")." + poly_specs_err_msg] + solution_error_message_pieces +
            [solution_err_msg_trailer_errors])
      )
      return True

  def add_explicit_symbolic_constraints(shape_env: DimVarEnv):
    if not shape_env: return
    assert scope is not None
    for constr in scope._explicit_constraints:
      # We can't just construct constr.e1 - constr.e2 because for an equality
      # constraint it would be reduced to 0.
      c_diff = constr.diff._evaluate(shape_env) if not core.is_constant_dim(constr.diff) else constr.diff  # pyrefly: ignore[missing-attribute]
      shape_constraints.add_constraint(
          constr.cmp, c_diff, 0,
          error_message_pieces=[
                f"Input shapes do not match the symbolic shape constraint {constr.debug_str}. "
                f"Expected '{constr.diff}' to be "
                f"{'greater or equal' if constr.cmp == Comparator.GEQ else 'equal'} to 0, "
                "but found ", c_diff,

                ". " + poly_specs_err_msg
              ] + solution_error_message_pieces + [
              solution_err_msg_trailer_errors])


  while True:
    nr_eqns = len(eqns)
    eqns = [eqn for eqn in eqns if not process_one_eqn(eqn)]
    if not eqns:
      add_explicit_symbolic_constraints(shape_env)
      # SUCCESS
      return shape_env, shape_constraints
    elif len(eqns) >= nr_eqns:
      break

  # We have some equations that we cannot solve further
  unsolved_vars: set[str] = set()
  unsolved_polys: list[_DimExpr] = []
  for eqn in eqns:
    unsolved_vars = unsolved_vars.union(eqn.aval_dim_expr._get_vars())
    unsolved_polys.append(eqn.aval_dim_expr)
  unsolved_vars = unsolved_vars.difference(shape_env.keys())
  err_msg = (
      f"Cannot solve for values of dimension variables {unsolved_vars}. "
      "We can only solve linear uni-variate constraints." + poly_specs_err_msg +
      " Unprocessed specifications: " +
      ", ".join(f"'{eqn.aval_dim_expr}' for dimension size {eqn.dim_name}"
                for eqn in eqns) +
      ". Please see https://docs.jax.dev/en/latest/export/shape_poly.html#dimension-variables-must-be-solvable-from-the-input-shapes for more details."
  )
  raise ValueError(err_msg)

