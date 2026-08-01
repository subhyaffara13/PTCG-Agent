
def get_op_names(op: torch._ops.OperatorBase) -> tuple[str, str]:
    op_overload_packet_name: str = op.name()
    op_overload_name = (
        f"{op_overload_packet_name}.{op._overloadname}"
        if isinstance(op, torch._ops.OpOverload)
        else op_overload_packet_name
    )
    return op_overload_packet_name, op_overload_name

