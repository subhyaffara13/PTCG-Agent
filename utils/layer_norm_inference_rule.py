
def layer_norm_inference_rule(
    n: Node,
    module_instance: torch.nn.LayerNorm,
    symbols: _SymbolDict,
    constraints: list[Constraint],
    counter: int,
) -> tuple[list[Constraint], int]:
    """
    Input and output shapes should be equal.
    Input should be consistent with the normalized_shape
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    return gen_layer_norm_constraints(
        n, module_instance.normalized_shape, symbols, counter
    )

