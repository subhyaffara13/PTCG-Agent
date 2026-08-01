
def relu_inference_rule(n: Node, module_instance):
    """
    Input and output shapes should be equal.
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    if n.args[0].type == Dyn and isinstance(n.type, TensorType):
        n.args[0].type = expand_to_tensor_dim(n.args[0].type, len(n.type.__args__))

    if isinstance(n.args[0].type, TensorType):
        n.type = get_greatest_upper_bound(n.args[0].type, n.type)
    return n.type


def relu_inference_rule(
    n: Node,
    module_instance: torch.nn.Module,
    symbols: _SymbolDict,
    constraints: list[Constraint],
    counter: int,
) -> tuple[list[Constraint], int]:
    """
    Input and output shapes should be equal.
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    output, counter = gen_tvar(counter)
    symbols[n] = output
    input = symbols[n.args[0]]
    if not isinstance(input, TVar):
        raise AssertionError(f"Expected TVar, got {type(input)}")
    return [BinConstraintT(input, output, op_eq)], counter

