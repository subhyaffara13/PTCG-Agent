
def register_pointwise_numeric_ldf64(op: torch._ops.OpOverloadPacket):
    register_op_requires_libdevice_fp64(op.__name__)
    return register_pointwise(
        op,
        type_promotion_kind=ELEMENTWISE_TYPE_PROMOTION_KIND.INT_TO_FLOAT,
    )

