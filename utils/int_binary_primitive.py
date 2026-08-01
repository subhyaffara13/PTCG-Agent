
def int_binary_primitive(
    op: str, primitive_name: str, return_type: RType = int_rprimitive, error_kind: int = ERR_NEVER
) -> PrimitiveDescription:
    return binary_op(
        name=op,
        arg_types=[int_rprimitive, int_rprimitive],
        return_type=return_type,
        primitive_name=primitive_name,
        error_kind=error_kind,
    )

