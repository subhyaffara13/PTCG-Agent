
def mark_mixed_dtype_allowed_computation_ops(gm):
    """
    Mark convolutions/linear which we will binary fold even with mixed precision constants. We constant fold in the higher precision
    for better accuracy and then recover the original precision after.
    """
    for target in [aten.convolution.default, aten.addmm.default, aten.mm.default]:
        for node in gm.graph.find_nodes(op="call_function", target=target):
            mark_mixed_dtype(node)

