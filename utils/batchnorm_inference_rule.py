
def batchnorm_inference_rule(
    n: Node,
    module_instance: BatchNorm2d,
    symbols: _SymbolDict,
    constraints: list[Constraint],
    counter: int,
) -> tuple[list[Constraint], int]:
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    # generate the new variable
    batchnorm_output, counter = gen_tvar(counter)
    symbols[n] = batchnorm_output
    batchnorm_input = symbols[n.args[0]]

    # dim vars
    d1, counter = gen_dvar(counter)
    d2, counter = gen_dvar(counter)
    d3, counter = gen_dvar(counter)
    d4, counter = gen_dvar(counter)

    nat_constraints = gen_nat_constraints([d1, d2, d3, d4])

    c1 = BinConstraintT(batchnorm_input, TensorType([d1, d2, d3, d4]), op_matching)
    c2 = BinConstraintT(batchnorm_input, batchnorm_output, op_eq)
    return [c1, c2, *nat_constraints], counter

