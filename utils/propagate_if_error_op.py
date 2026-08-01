
def propagate_if_error_op(builder: LowLevelIRBuilder, args: list[Value], line: int) -> Value:
    # Return False on NULL. The primitive uses ERR_FALSE, so this is an error.
    return builder.add(
        ComparisonOp(args[0], Integer(0, object_rprimitive), ComparisonOp.NEQ, line)
    )

