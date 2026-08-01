
def embedding_inference_rule(
    n: Node,
    module_instance: torch.nn.Embedding,
    symbols: _SymbolDict,
    constraints: list[Constraint],
    counter: int,
) -> tuple[list[Constraint], int]:
    """
    The output shape differs from the input shape in the last dimension
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    return gen_embedding_rules(n, symbols, module_instance.embedding_dim, counter)

