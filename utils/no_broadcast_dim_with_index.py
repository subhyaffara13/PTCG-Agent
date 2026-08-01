
def no_broadcast_dim_with_index(
    d1: list[DVar], d2: list[DVar], d3: list[DVar], d4: list[DVar], i: int
) -> Constraint:
    """
    Args:
        d1: input 1
        d2: input 2
        d3: simulated broadcasting for input 1
        d4: simulated broadcasting for input 2
        i: the rank of the resulting tensor addition

    Returns: Constraints for when no broadcasting occurs
    """
    return Conj(
        [
            Disj(
                [
                    Conj(
                        [
                            BinConstraintD(d1[i], 1, op_eq),
                            BinConstraintD(d2[i], 1, op_eq),
                        ]
                    ),
                    Conj(
                        [
                            BinConstraintD(d1[i], 1, op_neq),
                            BinConstraintD(d2[i], 1, op_neq),
                        ]
                    ),
                ]
            ),
            BinConstraintD(d1[i], d3[i], op_eq),
            BinConstraintD(d2[i], d4[i], op_eq),
        ]
    )

