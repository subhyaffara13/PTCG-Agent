
def is_dim_div_by_target(
    target: Sequence[DVar | int | _DynType], dim: DVar | Prod
) -> BinConstraintD:
    """
    Generate constraints to check if the input dimensions is divisible by the target dimensions
    Args:
        target: Target dimensions
        dim:  Input dimensions

    Returns: Constraints to check divisibility

    """
    return BinConstraintD(BinConstraintD(dim, Prod(target), op_mod), 0, op_eq)

