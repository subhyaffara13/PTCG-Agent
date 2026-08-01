
def is_view_node(n: fx.Node) -> bool:
    """Check if a node is a view operation (zero cost, no memory allocation)."""

    return isinstance(n.target, torch._ops.OpOverload) and (
        n.target.is_view and n.target.namespace in ("aten", "prims")
    )

