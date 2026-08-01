
def add_linear_constraints(
    dims1: list[DVar],
    dims2: list[DVar],
    in_features: int | DVar,
    out_features: int | DVar,
) -> list[Constraint]:
    if len(dims1) != len(dims2):
        raise AssertionError(f"Expected same length, got {len(dims1)} vs {len(dims2)}")
    constraints: list[Constraint] = []
    for i in range(len(dims1)):
        if i == len(dims1) - 1:
            constraints.append(BinConstraintD(dims1[i], in_features, op_consistency))
            constraints.append(BinConstraintD(dims2[i], out_features, op_eq))
        else:
            constraints.append(BinConstraintD(dims1[i], dims2[i], op_eq))

    return constraints

