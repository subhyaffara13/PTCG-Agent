
def is_aten_op_or_tensor_method(obj: Any) -> bool:
    return obj in get_tensor_method() or isinstance(
        obj,
        (torch._ops.OpOverloadPacket, torch._ops.OpOverload),
    )

