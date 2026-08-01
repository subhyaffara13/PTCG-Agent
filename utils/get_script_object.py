
def get_script_object(
    gm: torch.nn.Module, node: torch.fx.Node
) -> torch._C.ScriptObject:
    if not isinstance(node, torch.fx.Node):
        raise AssertionError(f"expected fx.Node, got {type(node).__name__}")
    if node.op != "get_attr":
        raise AssertionError(f"expected get_attr op, got {node.op}")
    attr_name = node.target
    if not isinstance(attr_name, str):
        raise AssertionError(f"expected str target, got {type(attr_name).__name__}")

    mod = gm
    for attr in attr_name.split("."):
        mod = getattr(mod, attr)
    if not isinstance(mod, torch._C.ScriptObject):
        raise AssertionError(f"expected ScriptObject, got {type(mod).__name__}")
    return mod

