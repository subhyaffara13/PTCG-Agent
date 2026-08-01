
def replace_node_module(
    node: fx.Node, modules: dict[str, Any], new_module: torch.nn.Module
):
    if not isinstance(node.target, str):
        raise AssertionError(f"Expected str target, got {type(node.target)}")
    parent_name, name = _parent_name(node.target)
    modules[node.target] = new_module
    setattr(modules[parent_name], name, new_module)

