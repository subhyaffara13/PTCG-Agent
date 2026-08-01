
def view_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    Similar to reshape but with an extra condition on the strides
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    # generate the new variable
    my_view, counter = gen_tvar(counter)
    symbols[n] = my_view

    src_var = symbols[n.args[0]]
    t2 = [
        symbols[elem] if isinstance(elem, Node) else elem for elem in n.args[1:]
    ]  # target shape
    t2_type = []
    num_constraints = []

    for t in t2:
        if t == -1:
            var, counter = gen_dvar(counter)
            t2_type.append(var)
            # pyrefly: ignore [bad-argument-type]
            num_constraints.append(BinConstraintD(var, Dyn, op_neq))

        else:
            # pyrefly: ignore [bad-argument-type]
            num_constraints.append(BinConstraintD(t, Dyn, op_neq))
            t2_type.append(t)  # type: ignore[arg-type]

    t2_type = TensorType(t2_type)  # type: ignore[assignment]

    c1 = BinConstraintT(my_view, t2_type, op_eq)
    c2 = CanReshape(src_var, t2_type)  # pyrefly: ignore[bad-argument-type]

    # TODO: add the extra check mentioned here:
    # https://pytorch.org/docs/stable/generated/torch.Tensor.view.html#torch.Tensor.view

    return [c1, c2] + num_constraints, counter  # type: ignore[operator]

