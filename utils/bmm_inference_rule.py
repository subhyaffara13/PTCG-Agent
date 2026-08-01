
def bmm_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    Constraints that match the input to a size 3 tensor
    and switch the dimensions according to the rules
    of batch multiplication
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    if not isinstance(n.args[1], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[1])}")

    bmm_output, counter = gen_tvar(counter)
    symbols[n] = bmm_output

    bmm_input1 = symbols[n.args[0]]
    bmm_input2 = symbols[n.args[1]]

    dims_input1, counter = gen_tensor_dims(3, counter)
    dims_input2, counter = gen_tensor_dims(3, counter)

    inputs_dyn = Conj(
        [
            BinConstraintT(bmm_input1, Dyn, op_eq),
            BinConstraintT(bmm_input2, Dyn, op_eq),
            BinConstraintT(bmm_output, Dyn, op_eq),
        ]
    )

    input1_dyn = Conj(
        [
            BinConstraintT(bmm_input1, Dyn, op_eq),
            BinConstraintT(bmm_input2, TensorType(dims_input2), op_eq),
            BinConstraintT(
                bmm_output, TensorType([dims_input2[0], Dyn, dims_input2[2]]), op_eq
            ),
        ]
    )

    input2_dyn = Conj(
        [
            BinConstraintT(bmm_input2, Dyn, op_eq),
            BinConstraintT(bmm_input1, TensorType(dims_input1), op_eq),
            BinConstraintT(
                bmm_output, TensorType([dims_input1[0], dims_input1[1], Dyn]), op_eq
            ),
        ]
    )

    consistency_constraints = [
        BinConstraintD(dims_input1[0], dims_input2[0], op_consistency)
    ]

    batch_size, counter = gen_dvar(counter)

    inputs_are_tensors = Conj(
        [
            BinConstraintT(bmm_input1, TensorType(dims_input1), op_eq),
            BinConstraintT(bmm_input2, TensorType(dims_input2), op_eq),
            BinConstraintT(
                bmm_output,
                TensorType([batch_size, dims_input1[1], dims_input2[2]]),
                op_eq,
            ),
            *consistency_constraints,
            DGreatestUpperBound(batch_size, dims_input1[0], dims_input2[0]),
        ]
    )

    return [Disj([inputs_dyn, input1_dyn, input2_dyn, inputs_are_tensors])], counter

