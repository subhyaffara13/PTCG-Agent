
def scatter_always_uses_mutation(node: torch.fx.Node) -> bool:
    _, _, view_ops = node.args
    view_ops = cast(Sequence[torch.fx.node.Argument], view_ops)
    return any(
        target in _ALWAYS_MUTATING_SCATTER_OPS
        for view in view_ops
        if isinstance(target := getattr(view, "target", None), torch._ops.OpOverload)
    )

