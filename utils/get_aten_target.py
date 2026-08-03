from typing import Any, Callable

def get_aten_target(node: fx.Node) -> OpOverloadPacket | Callable[..., Any] | str:
    if hasattr(node.target, "overloadpacket"):
        return node.target.overloadpacket
    return node.target

