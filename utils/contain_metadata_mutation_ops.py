
def contain_metadata_mutation_ops(module: torch.fx.GraphModule) -> bool:
    """
    Checks if the module contains any metadata mutation ops.
    """
    for node in module.graph.nodes:
        if (
            node.op == "call_function"
            and hasattr(node.target, "tags")
            and torch.Tag.inplace_view in node.target.tags
        ):
            return True
    return False

