
def index_put_fallback(self, indices, values, accumulate):
    from .utils import _fx_node_is_input_dependent_cudagraph_unsafe

    op_overload = getattr(aten.index_put_, V.graph.current_node.target._overloadname)  # type: ignore[union-attr]

    # Check if any index is a boolean tensor - if so, mark as cudagraph-unsafe
    # because boolean indices trigger .nonzero() during CUDA graph capture
    # When graph_partition is enabled, skip - partitioning handles this
    fx_node = V.graph.current_node
    if (
        not config.graph_partition
        and fx_node is not None
        and _fx_node_is_input_dependent_cudagraph_unsafe(fx_node)
    ):
        msg = "index_put_ fallback with boolean indexing is not compatible with CUDA graphs"
        if stack_trace := fx_node.meta.get("stack_trace", None):
            msg = f"{msg} Found from : \n {stack_trace}"
        V.graph.disable_cudagraphs_reason = msg

    ir.IndexPutFallback(op_overload, self, indices, values, accumulate)
    return self

