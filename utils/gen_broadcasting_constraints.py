import itertools

def gen_broadcasting_constraints(
    e1: TVar, e2: TVar, symbols: _SymbolDict, counter: int, output_var: TVar
) -> tuple[list[Constraint], int]:
    # additional vars that don't correspond to expressions
    e11, counter = gen_tvar(counter)
    e22, counter = gen_tvar(counter)

    # generate constraints
    c1 = TGreatestUpperBound(output_var, e11, e22)
    c2 = ApplyBroadcasting(e11, e22, e1, e2)
    c3 = BinConstraintT(e11, e22, op_consistency)
    return [c1, c2, c3], counter


def gen_broadcasting_constraints(
    e1: TVar, e2: TVar, e11: TVar, e12: TVar, i: int, counter: int
) -> tuple[Constraint, Constraint, Constraint, list[BinConstraintD], int]:
    """
    Simulates broadcasting on e1 and e2 and returns the results
    respectively in e11 and e12. Because of gradual types,
    e1 and e2 may not be equal. Similarly, e11 and e12 may not
    be equal. e11 and e12 should be guaranteed to be consistent
    as they represent the shapes of the tensors to be added after
    broadcasting.
    Args:
        e1: TVar representing the type of input 1
        e2: TVar representing the type of input 2
        e11: TVar representing the representing broadcasted input 1
        e12: TVar representing the representing broadcasted input 2
        i: The rank of the resulting type of addition
        counter: for variable tracking

    Returns: Simplified broadcasting constraints

    """
    dims, counter = gen_lists_of_dims(4, i, counter)
    [d1, d2, d3, d4] = dims
    nat_dims_i = gen_nat_constraints(list(itertools.chain.from_iterable(dims)))

    initialize_tensors_constraints = create_equality_constraints_for_broadcasting(
        e1, e2, e11, e12, d1, d2, d3, d4
    )

    [e1_tensor, e11_tensor, e2_tensor, e12_tensor] = initialize_tensors_constraints

    # without padding, broadcast all possibilities for tensors of size i
    final_tensor_constraint_no_padding = Conj(
        [
            *initialize_tensors_constraints,
            generate_all_broadcasting_possibilities_no_padding(d1, d2, d3, d4),
        ]
    )

    # with padding, broadcast all possibilities for tensors of size i
    final_tensor_constraint_padding_arg1, counter = apply_padding(
        e1, e11_tensor, e2_tensor, e12_tensor, d2, d3, d4, counter
    )

    final_tensor_constraint_padding_arg2, counter = apply_padding(
        e2, e12_tensor, e1_tensor, e11_tensor, d1, d4, d3, counter
    )

    return (
        final_tensor_constraint_no_padding,
        final_tensor_constraint_padding_arg1,
        final_tensor_constraint_padding_arg2,
        nat_dims_i,
        counter,
    )

