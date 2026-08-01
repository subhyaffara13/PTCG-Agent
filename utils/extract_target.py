
def extract_target(node: torch.fx.Node) -> torch.fx.node.Target:
    """For call_function and call_method, we directly use the target function;
    For call_module, the target is string, and we treat the module class
     as a function.
    """
    if node.op == "call_module":
        assert isinstance(node.target, str)
        return _get_attr(node.graph.owning_module, node.target).__class__
    return node.target

