
def gen_greatest_upper_bound(
    constraint: TGreatestUpperBound, counter: int
) -> tuple[list[Constraint], int]:
    """
    Args:
        constraint: Greatest upper bound on tensors
        counter: variable tracking

    Returns: A set of equality constraints and DGreatestUpperBound constraints

    """

    all_constraints: list[Constraint] = []

    for i in range(1, MAX_TENSOR_RANK + 1):
        c: list[Constraint] = []
        dims1, counter = gen_tensor_dims(i, counter)
        c1tensor = TensorType(dims1)

        dims2, counter = gen_tensor_dims(i, counter)
        c2tensor = TensorType(dims2)

        dims3, counter = gen_tensor_dims(i, counter)
        c3tensor = TensorType(dims3)

        c += [
            BinConstraintT(constraint.rhs1, c1tensor, op_eq),
            BinConstraintT(constraint.rhs2, c2tensor, op_eq),
            BinConstraintT(constraint.res, c3tensor, op_eq),
        ] + gen_nat_constraints(dims1 + dims2 + dims3)

        if not (
            len(c3tensor.__args__) == len(c1tensor.__args__) == len(c2tensor.__args__)
        ):
            raise AssertionError("Tensor args lengths must be equal")
        for i in range(len(c3tensor.__args__)):
            c.append(
                DGreatestUpperBound(
                    c3tensor.__args__[i], c1tensor.__args__[i], c2tensor.__args__[i]
                )
            )

        all_constraints.append(Conj(c))
    return all_constraints, counter

