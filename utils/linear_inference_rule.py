
def linear_inference_rule(n: Node, module_instance):
    """
    Applies the shape information to the input then gets the greatest upper bound
    of the resulting type and the existing type
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    if n.args[0].type == Dyn and isinstance(n.type, TensorType):
        n.args[0].type = expand_to_tensor_dim(n.args[0].type, len(n.type.__args__))
    if isinstance(n.args[0].type, TensorType):
        output_type = linear_check(n.args[0].type, module_instance)
        n.type = get_greatest_upper_bound(output_type, n.type)
    return n.type


def linear_inference_rule(
    n: Node,
    module_instance: torch.nn.Linear,
    symbols: _SymbolDict,
    constraints: list[Constraint],
    counter: int,
) -> tuple[list[Constraint], int]:
    """
    Input and output sizes should be the same except for the last dimension
    If the input is Dyn, then so should the output
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    return linear_constraints(
        n, module_instance.in_features, module_instance.out_features, symbols, counter
    )

