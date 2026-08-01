
def _get_pointwise_ops_from_tag() -> list[OpOverload]:
    """
    Auto-discover pointwise ops via torch.Tag.pointwise, from ops.aten, ops.prims.
    """
    ops = []
    for ns in [torch.ops.aten, torch.ops.prims]:
        for attr_name in dir(ns):
            attr = getattr(ns, attr_name)
            if isinstance(attr, torch._ops.OpOverloadPacket):
                for overload_name in attr.overloads():
                    op = getattr(attr, overload_name)
                    if torch.Tag.pointwise in op.tags:
                        ops.append(op)
    return ops

