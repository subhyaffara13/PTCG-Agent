
def generate_all_int_dyn_dim_possibilities(
    my_list: list[DVar],
) -> list[tuple[BinConstraintD, ...]]:
    """
    Generate all possibilities of being equal or not equal to dyn for my_list
    Args:
        my_list: List of tensor dimensions

    Returns: A list of a list of constraints. Each list of constraints corresponds to
    one possibility about the values of the dimension variables
    """
    # generate all possibilities of being equal or not equal to dyn for my_list
    eq_possibilities = [
        BinConstraintD(my_list[i], Dyn, op_eq) for i in range(len(my_list))
    ]
    neq_possibilities = [
        BinConstraintD(my_list[i], Dyn, op_neq) for i in range(len(my_list))
    ]

    d_possibilities = [list(i) for i in zip(eq_possibilities, neq_possibilities)]
    all_possibilities = list(itertools.product(*d_possibilities))
    return all_possibilities

