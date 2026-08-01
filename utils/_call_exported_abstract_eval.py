
def _call_exported_abstract_eval(
    *in_avals: core.AbstractValue,
    exported: Exported
) -> tuple[tuple[core.AbstractValue, ...], set[effects.Effect]]:
  exported_dim_vars = shape_poly.all_dim_vars(exported.in_avals)
  assert len(in_avals) == len(exported.in_avals)  # since the pytrees have the same structure
  # Check that the expected shapes match the actual ones
  for arg_idx, (exp_aval, actual_aval) in enumerate(zip(exported.in_avals, in_avals)):
    if not isinstance(actual_aval, core.ShapedArray):
      raise ValueError(f"Expected ShapedArray but got: {actual_aval}")
    def pp_arg_dim(dim_idx: int | None) -> str:
      return shape_poly.pretty_print_dimension_descriptor(exported.in_tree,
                                                          arg_idx, dim_idx)
    if len(exp_aval.shape) != len(actual_aval.shape):
      raise ValueError(
          f"Rank mismatch for {pp_arg_dim(None)}: expected {exp_aval.shape} "
          f"and called with {actual_aval.shape}")
    if exp_aval.dtype != actual_aval.dtype:
      raise ValueError(
          f"Dtype mismatch for {pp_arg_dim(None)}: expected {exp_aval.dtype} "
          f"and called with {actual_aval.dtype}")
    for dim_idx, aval_d in enumerate(exp_aval.shape):
      # If the exp_aval has a constant dimension then the actual argument must have
      # a matching constant dimension.
      if core.is_constant_dim(aval_d):
        if (not core.is_constant_dim(actual_aval.shape[dim_idx]) or
            aval_d != actual_aval.shape[dim_idx]):
          raise ValueError(
              f"Shape mismatch for {pp_arg_dim(dim_idx)} "
              "(expected same constant): "
              f"expected {exp_aval.shape} and called with {actual_aval.shape}")

  # Must express the exported_dim_vars in terms of the shapes in in_avals.
  solution, shape_constraints, synth_dim_vars = shape_poly.solve_dim_vars(
      exported.in_avals, args_kwargs_tree=exported.in_tree)
  synthetic_env: shape_poly.DimVarEnv = {
      vname: in_avals[arg_idx].shape[dim_idx]
      for (vname, arg_idx, dim_idx) in synth_dim_vars}
  synthetic_eval = shape_poly.ShapeEvaluator(synthetic_env)
  # We discharge all the constraints statically. This results in much simpler
  # composability (because we do not have to worry about the constraints of the
  # Exported called recursively; we only need to worry about entry-point
  # constraints). This also makes sense from a composability point of view,
  # because we get the same errors if we invoke the exported module, or if we
  # trace the exported function. Consider for example, an exported module with
  # signature `f32[a, a] -> f32[a]`. If we invoke the module with an argument
  # `f32[c, d]` it is better to fail because `c == d` is inconclusive, than
  # succeed and add a compile-time check that `c == d`. In the latter case,
  # it would be ambiguous whether we should continue tracing with a result
  # of type `f32[c]` or `f32[d]`.
  shape_constraints.check_statically(synthetic_eval)
  exported_dim_values = [synthetic_eval.evaluate(solution[var])
                         for var in exported_dim_vars]

  def make_aval(out_aval_idx: int):
    out_aval = exported.out_avals[out_aval_idx]
    if exported._has_named_shardings:
      sharding = exported._out_named_shardings[out_aval_idx]
    else:
      sharding = None
    aval = core.ShapedArray(
      core.evaluate_shape(out_aval.shape, exported_dim_vars,
                          *exported_dim_values),
      dtype=out_aval.dtype, weak_type=out_aval.weak_type,
      # memory_space from out_aval because sharding may be None
      memory_space=out_aval.memory_space)
    return core.update_aval_with_sharding(aval, sharding)

  out_avals = tuple(make_aval(out_aval_idx)
                    for out_aval_idx in range(len(exported.out_avals)))
  return out_avals, set(exported.ordered_effects + exported.unordered_effects)

