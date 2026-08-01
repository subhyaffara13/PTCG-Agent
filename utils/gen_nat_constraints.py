
def gen_nat_constraints(list_of_dims: list[DVar]) -> list[BinConstraintD]:
    """
    Generate natural number constraints for dimensions
    """
    return [BinConstraintD(0, d, op_leq) for d in list_of_dims]

