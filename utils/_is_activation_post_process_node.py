
def _is_activation_post_process_node(
    node: Node, named_modules: dict[str, torch.nn.Module]
) -> bool:
    return (
        isinstance(node, torch.fx.Node)
        and node.op == "call_module"
        and _is_activation_post_process(named_modules[str(node.target)])
    )

