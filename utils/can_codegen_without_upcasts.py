
def can_codegen_without_upcasts(
    prologue: "SchedulerNode",
    disallow_fp32_ops: bool = False,
) -> bool:
    """
    Can this prologue be run without `upcast_to_fp32` while preserving numerics.

    This is only true if the node only contains dtype conversions, indexing, and other non-arithmetic operators.

    If disallow_fp32_ops is True, then we also disallow ops that are explicitly computed in fp32 or fp64.
    """
    if prologue.get_operation_names() <= V.graph.low_precision_codegen_ops:
        return True

    low_prec_analysis = RecordLowPrecisionOps(disallow_fp32_ops)

    # Need to turn off upcasting to do analysis of whether we can turn it off
    with (
        config.patch("triton.codegen_upcast_to_fp32", False),
        V.set_ops_handler(low_prec_analysis),
    ):
        prologue._body(*prologue.get_ranges())

    return not low_prec_analysis.low_precision_numeric_op

