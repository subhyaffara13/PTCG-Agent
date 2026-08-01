
def create_equality_constraints_for_broadcasting(
    e1: TVar,
    e2: TVar,
    e11: TVar,
    e12: TVar,
    d1: list[DVar],
    d2: list[DVar],
    d11: list[DVar],
    d12: list[DVar],
) -> list[BinConstraintT]:
    """
    Create equality constraints for when no broadcasting occurs
    Args:
        e1: Input 1
        e2: Input 2
        e11: Broadcasted input 1
        e12: Broadcasted input 2
        d1: Variables that store dimensions for e1
        d2: Variables that store dimensions for e2
        d11: Variables that store dimensions for e11
        d12: Variables that store dimensions for e22

    Returns: Four equality constraints

    """

    e1_tensor = BinConstraintT(e1, TensorType(d1), op_eq)
    e11_tensor = BinConstraintT(e11, TensorType(d11), op_eq)
    e2_tensor = BinConstraintT(e2, TensorType(d2), op_eq)
    e12_tensor = BinConstraintT(e12, TensorType(d12), op_eq)
    return [e1_tensor, e11_tensor, e2_tensor, e12_tensor]

