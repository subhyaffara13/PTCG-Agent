
def infer_constraints(
    template: Type,
    actual: Type,
    direction: int,
    skip_neg_op: bool = False,
    erase_types: bool = True,
) -> list[Constraint]:
    """Infer type constraints.

    Match a template type, which may contain type variable references,
    recursively against a type which does not contain (the same) type
    variable references. The result is a list of type constrains of
    form 'T is a supertype/subtype of x', where T is a type variable
    present in the template and x is a type without reference to type
    variables present in the template.

    Assume T and S are type variables. Now the following results can be
    calculated (read as '(template, actual) --> result'):

      (T, X)            -->  T :> X
      (X[T], X[Y])      -->  T <: Y and T :> Y
      ((T, T), (X, Y))  -->  T :> X and T :> Y
      ((T, S), (X, Y))  -->  T :> X and S :> Y
      (X[T], Any)       -->  T <: Any and T :> Any

    The constraints are represented as Constraint objects. If skip_neg_op == True,
    then skip adding reverse (polymorphic) constraints (since this is already a call
    to infer such constraints).
    """
    if any(
        get_proper_type(template) == get_proper_type(t)
        and get_proper_type(actual) == get_proper_type(a)
        for (t, a) in reversed(type_state.inferring)
    ):
        return []
    if has_recursive_types(template) or isinstance(get_proper_type(template), Instance):
        # This case requires special care because it may cause infinite recursion.
        # Note that we include Instances because the may be recursive as str(Sequence[str]).
        if not has_type_vars(template):
            # Return early on an empty branch.
            return []
        type_state.inferring.append((template, actual))
        res = _infer_constraints(template, actual, direction, skip_neg_op, erase_types)
        type_state.inferring.pop()
        return res
    return _infer_constraints(template, actual, direction, skip_neg_op, erase_types)

