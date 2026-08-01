
def _get_collective_estimations(coll_node: fx.Node) -> tuple[float, float]:
    """Get NCCL and Inductor analytical estimations for a collective node.

    Returns: (nccl_ms, inductor_ms)
    """
    nccl_ms = (
        torch._inductor.comm_analysis.estimate_nccl_collective_runtime_from_fx_node(
            coll_node, None, use_nccl_estimator=True
        )
    )
    inductor_ms = (
        torch._inductor.comm_analysis.estimate_nccl_collective_runtime_from_fx_node(
            coll_node, None, use_nccl_estimator=False
        )
    )
    return nccl_ms, inductor_ms

