
def filter_nodes(nodes: Iterable[torch.fx.Node], fn: Any) -> list[torch.fx.Node]:
    fns = [fn]
    if isinstance(fn, torch._ops.OpOverloadPacket):
        fns.extend([getattr(fn, overload) for overload in fn.overloads()])

    return [node for node in nodes if node.target in fns]

