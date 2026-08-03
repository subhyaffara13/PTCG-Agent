import logging
from typing import Any

def infer_layout(
    module: ir.Module, *, fuel: int = _DEFAULT_LAYOUT_INFERENCE_FUEL,
    arch: tuple[int, int] = (9, 0)
):
  """Infers layouts for the given module.

  * If there are vector (respectively SMEM refs, TMEM refs) operands,
  `in_layouts` (respectively `in_transforms`, `in_tmem_layouts`) will be set and
  contain one element per relevant argument in the memory space.
  * If there are vector (respectively SMEM refs, TMEM refs) outputs,
  `out_layouts` (respectively `out_transforms`, `out_tmem_layouts`) will be set
  and contain one element per relevant argument in the memory space.
  * Any of these attributes is guaranteed to not be set if there is no relevant
  input/output in the corresponding memory space.

  Args:
    module: The module to infer layouts for.
    fuel: The fuel is provided in order to limit the number of attempts made by
      the solver.
    arch: The architecture to infer layouts for.
  """
  global_constraint_system: cs.ConstraintSystem | cs.Unsatisfiable
  global_constraint_system = cs.ConstraintSystem()
  ctx = DerivationContext()

  def gather_constraints(op: Any):
    # Terminator ops are handled directly by the op whose region they belong to.
    # This is because they need to be in sync with their parent op's inputs and
    # outputs---and the parent op's constraints therefore need to take them into
    # account.
    if is_terminator(op):
      return
    should_have_layout = (
        inference_utils.should_have_layout(op)
        or inference_utils.should_have_tmem_layout(op)
        or inference_utils.should_have_transforms(op)
    )
    if not should_have_layout:
      return
    rule = _constraint_system_derivation_rules.get(op.OPERATION_NAME, None)
    if rule is None:
      raise NotImplementedError(f"No layout inference rule defined for {op}")
    rule_result = rule(ctx, op)
    nonlocal global_constraint_system
    constraint_system, mapping = rule_result
    for var, sites in mapping.items():
      assert isinstance(var.key, ValueSite)
      for site in sites:
        if site.memory_space != var.memory_space:
          raise ValueError(
              f"Memory space mismatch between variable and {site}:"
              f" {var.memory_space} != {site.memory_space}."
          )
        if site.shape != var.shape:
          raise ValueError(
              f"Shape mismatch between variable and {site}:"
              f" {var.shape} != {site.shape}."
          )
    global_constraint_system &= constraint_system
    ctx.update(mapping)

  for op in module.body:
    traverse_op(op, gather_constraints)
    # Short-circuit if we have an unsatisfiable constraint system, we won't
    # construct anything useful anymore.
    if isinstance(global_constraint_system, cs.Unsatisfiable):
      break

  if isinstance(global_constraint_system, cs.Unsatisfiable):
    raise ValueError(
        "Failed to infer a possible set of layouts. This should only happen if "
        "user-provided layout casts are unsatisfiable."
    )

  constraints = derive_relayout_constraints(ctx.value_sites_for_variable)
  global_constraint_system &= cs.ConstraintSystem(constraints=constraints)
  assert not isinstance(global_constraint_system, cs.Unsatisfiable)

  # Add additional (redundant) constraints which helps the search converge
  # faster.
  global_constraint_system = cs.saturate_distinct_from_splat(
      global_constraint_system
  )
  assert not isinstance(global_constraint_system, cs.Unsatisfiable)
  global_constraint_system = cs.saturate_divides_constraints_for_equal_vars(
      global_constraint_system
  )

  # Attempt to find assignments that satisfy the constraint system.
  solution, remaining_fuel = find_assignments_for(
      list(ctx.value_sites_for_variable.keys()),
      global_constraint_system,
      fuel=fuel,
      arch=arch,
  )

  if logging.vlog_is_on(1):
    print("Finding a solution (or exhausting the entire search space) "
          f"consumed {fuel - remaining_fuel}/{fuel} fuel.")

  if isinstance(solution, cs.Unsatisfiable):
    raise ValueError(
        "Failed to infer a possible set of layouts. This should only happen if "
        "user-provided layout casts are unsatisfiable."
    )

  layout_for_value_site: dict[ValueSite, cs.Constant] = {}
  for variable, value_sites in ctx.value_sites_for_variable.items():
    layout = solution[variable]
    # Ensure that the layout assignment is valid for the variable. This should
    # only ever fail if our implementation is buggy.
    check_layout_assignment(variable, layout)
    for value_site in value_sites:
      layout_for_value_site[value_site] = layout

  # Assigns the layouts that we found to the ops.
  assign_layouts(layout_for_value_site)

  # Sanity check: ensure that all ops have the right number of in/out layouts.
  for op in module.body:
    traverse_op(op, _ensure_all_layouts_are_set)

