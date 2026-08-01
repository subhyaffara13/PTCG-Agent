
def pointwise_ops() -> list[torch._ops.OpOverloadPacket]:
    ops: list[torch._ops.OpOverloadPacket] = []
    for attr_name in dir(torch.ops.aten):
        opoverloadpacket = getattr(torch.ops.aten, attr_name)
        if not isinstance(opoverloadpacket, torch._ops.OpOverloadPacket):
            continue

        for overload in opoverloadpacket.overloads():
            op_overload = getattr(opoverloadpacket, overload)
            if torch.Tag.pointwise in op_overload.tags:
                # currently aot autograd uses packet not overload
                ops.append(opoverloadpacket)
                break

    return ops

