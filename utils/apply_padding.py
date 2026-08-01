
def apply_padding(
    e1_var: TVar,
    e11: BinConstraintT,
    e2: BinConstraintT,
    e12: BinConstraintT,
    d2: list[DVar],
    d11: list[DVar],
    d12: list[DVar],
    counter: int,
) -> tuple[Constraint, int]:
    """
    We are considering the possibility where one input has less dimensions than
    another input, so we apply padding to the broadcasted results

    Args:
        e1_var: Variable representing the first input where padding will be
        e11: constraint of the form e11 = Tensortype[d1, ..., dn]
        e2:  constraint of the form e2 = Tensortype[d1, ..., dn]
        e12: constraint of the form e11 = Tensortype[d1, ..., dn]
        d2: Tensor variables for the second input
        d11: Tensor variables for the broadcasted first input
        d12: Tensor variables for the broadcasted second input
        counter: variable tracking

    Returns: A new constraint whose goal is to apply padding to the broadcasted result

    """

    res = []

    # pad the shorter input with None so we can pass it to the broadcasting helper function
    for i in range(1, len(d2)):
        d1, counter = gen_tensor_dims(i, counter)

        nat_constraints = gen_nat_constraints(d1 + d2 + d11 + d12)

        e1 = BinConstraintT(e1_var, TensorType(d1), op_eq)

        simulate_padding = [None] * (len(d2) - i)

        if len(simulate_padding + d1) != len(d2):
            raise AssertionError("Padding + d1 length must equal d2 length")

        # for every padding size, we also consider broadcasting
        broadcast_padding = [
            broadcast_dim(simulate_padding, d2, d11, d12, j, True)
            for j in range(len(d2) - i)
        ]

        # we consider the possibilities for broadcasting for every dimension. Since we already
        # padded d1, we do not consider it while broadcasting
        all_broadcasting_possibilities = (
            generate_all_broadcasting_possibilities_no_padding(
                d1, d2[(len(d2) - i) :], d11[(len(d2) - i) :], d12[(len(d2) - i) :]
            )
        )
        # combine all constraints into a conjunction
        c = Conj(
            [
                e1,
                e11,
                e2,
                e12,
                *broadcast_padding,
                all_broadcasting_possibilities,
                *nat_constraints,
            ]
        )
        res.append(c)

    return Disj(res), counter

