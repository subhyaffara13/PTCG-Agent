
def reset_modules(
    nodes: list[fx.Node],
    modules: dict[str, nn.Module],
    old_modules: dict[nn.Module, nn.Module],
):
    """
    Maps each module that's been changed with `modules_to_mkldnn` back to its
    original.
    """
    for node in nodes:
        if node.op == "call_module":
            if not isinstance(node.target, str):
                raise AssertionError(f"Expected str target, got {type(node.target)}")
            cur_module = modules[node.target]
            if cur_module in old_modules:
                replace_node_module(node, modules, old_modules[cur_module])

