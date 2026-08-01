
def reset_provenance_globals() -> Iterator[None]:
    """Context manager that resets provenance tracking globals upon entering
    and restores their original values when exiting."""
    global _pre_grad_graph_id
    global _inductor_post_to_pre_grad_nodes
    global _inductor_triton_kernel_to_post_grad_node_info
    global _inductor_pre_grad_node_stack_trace
    global _inductor_kernel_stack_trace
    global _inductor_kernel_provenance_debug_handle

    # Store original values
    original_pre_grad_graph_id = _pre_grad_graph_id
    original_post_to_pre_grad_nodes = _inductor_post_to_pre_grad_nodes.copy()
    original_triton_kernel_to_post_grad_node_info = (
        _inductor_triton_kernel_to_post_grad_node_info.copy()
    )
    original_inductor_pre_grad_node_stack_trace = (
        _inductor_pre_grad_node_stack_trace.copy()
    )
    original_inductor_kernel_stack_trace = _inductor_kernel_stack_trace.copy()
    original_inductor_kernel_provenance_debug_handle = (
        _inductor_kernel_provenance_debug_handle
    )

    # Reset to default values
    _pre_grad_graph_id = -1
    _inductor_post_to_pre_grad_nodes = {}
    _inductor_triton_kernel_to_post_grad_node_info = {}
    _inductor_pre_grad_node_stack_trace = {}
    _inductor_kernel_stack_trace = {}
    _inductor_kernel_provenance_debug_handle = 0

    try:
        yield
    finally:
        # Restore original values
        _pre_grad_graph_id = original_pre_grad_graph_id
        _inductor_post_to_pre_grad_nodes = original_post_to_pre_grad_nodes
        _inductor_triton_kernel_to_post_grad_node_info = (
            original_triton_kernel_to_post_grad_node_info
        )
        _inductor_kernel_stack_trace = original_inductor_kernel_stack_trace
        _inductor_pre_grad_node_stack_trace = (
            original_inductor_pre_grad_node_stack_trace
        )
        _inductor_kernel_provenance_debug_handle = (
            original_inductor_kernel_provenance_debug_handle
        )

