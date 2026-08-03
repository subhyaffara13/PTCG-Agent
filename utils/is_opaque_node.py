from typing import Any

def is_opaque_node(node: Any) -> bool:
    """Check if a node contains an opaque or non-tensor value (e.g., ProcessGroup)."""
    from torch._library.fake_class_registry import FakeScriptObject

    if not isinstance(node, torch.fx.Node):
        return False
    if "val" not in getattr(node, "meta", {}):
        return False
    val = node.meta["val"]
    if is_opaque_value(val):
        return True
    if isinstance(val, (torch.ScriptObject, FakeScriptObject)):
        return True
    return False

