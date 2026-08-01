
def is_function_or_wrapper(
    value: Any,
) -> TypeIs[_FuncTypes | torch._ops.OpOverloadPacket | torch._ops.OpOverload]:
    return is_function(value) or isinstance(
        value, (torch._ops.OpOverloadPacket, torch._ops.OpOverload)
    )

