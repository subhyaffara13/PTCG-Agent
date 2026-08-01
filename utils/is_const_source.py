
def is_const_source(
    node: torch.fx.Node, lifted_constant_names: list[str] | None
) -> bool:
    return node.op == "get_attr" or node.name in (lifted_constant_names or ())

