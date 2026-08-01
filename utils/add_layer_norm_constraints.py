
def add_layer_norm_constraints(
    input_dim: list[DVar], normalized_dim: list[int]
) -> list[Constraint]:
    """
    The constraints say that the type has te form: [*, 1024, 1024]
     while the normalized_dim have the form [1024, 1024]
    Args:
        input_dim: Input shape of layer norm
        normalized_dim: normalized_dim parameter of the module instance

    """

    # in this case we return false since there's a pattern mismatch
    if len(normalized_dim) > len(input_dim):
        return [F()]

    else:
        constraints: list[Constraint] = []
        for i, n in zip(reversed(input_dim), reversed(normalized_dim)):
            constraints.append(BinConstraintD(i, n, op_consistency))
        return constraints

