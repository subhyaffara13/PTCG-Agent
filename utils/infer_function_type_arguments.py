
def infer_function_type_arguments(
    callee_type: CallableType,
    arg_types: Sequence[Type | None],
    arg_kinds: list[ArgKind],
    arg_names: Sequence[str | None] | None,
    formal_to_actual: list[list[int]],
    context: ArgumentInferContext,
    strict: bool = True,
    allow_polymorphic: bool = False,
) -> tuple[list[Type | None], list[TypeVarLikeType]]:
    """Infer the type arguments of a generic function.

    Return an array of lower bound types for the type variables -1 (at
    index 0), -2 (at index 1), etc. A lower bound is None if a value
    could not be inferred.

    Arguments:
      callee_type: the target generic function
      arg_types: argument types at the call site (each optional; if None,
                 we are not considering this argument in the current pass)
      arg_kinds: nodes.ARG_* values for arg_types
      formal_to_actual: mapping from formal to actual variable indices
    """
    # Infer constraints.
    constraints = infer_constraints_for_callable(
        callee_type, arg_types, arg_kinds, arg_names, formal_to_actual, context
    )

    # Solve constraints.
    type_vars = callee_type.variables
    return solve_constraints(type_vars, constraints, strict, allow_polymorphic)

