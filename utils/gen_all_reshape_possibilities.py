
def gen_all_reshape_possibilities(
    list_of_dims: list[DVar], target: Sequence[DVar | int | _DynType]
) -> Constraint:
    """
    Consider all possibilities what the input dimensions could be (number or dynamic)
    Then generate the appropriate constraints using multiplication or mod depending on the possibility
    The possibilities we consider here are the cross product of being equal to dyn or not equal to dyn
    for the input. Target is fixed because at most one dimension could be dyn.
    We have different cases for this.

    Args:
        list_of_dims: The input list of dimensions
        target: The tensor we want to reshape to

    Returns: A disjunction of transformed reshape constraints

    """
    all_possibilities = generate_all_int_dyn_dim_possibilities(list_of_dims)

    all_constraints = []

    for p in all_possibilities:
        to_multiply: list[DVar] = []

        p = list(p)

        for constraint in p:
            if not isinstance(constraint, BinConstraintD):
                raise AssertionError(f"Expected BinConstraintD, got {type(constraint)}")
            if constraint.op == op_neq:
                to_multiply.append(constraint.lhs)  # type: ignore[arg-type]

        if not to_multiply:
            all_constraints.append(Conj(p))

        elif len(to_multiply) < len(list_of_dims):
            all_constraints.append(
                Conj(p + [is_target_div_by_dim(target, Prod(to_multiply))])
            )
        else:
            all_constraints.append(
                Conj(p + [BinConstraintD(Prod(list_of_dims), Prod(target), op_eq)])
            )

    return Disj(all_constraints)

