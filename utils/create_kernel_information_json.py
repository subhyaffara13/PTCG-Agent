
def create_kernel_information_json() -> dict[str, dict[str, list[str]]]:
    """Create kernel information JSON"""
    try:
        global _inductor_post_to_pre_grad_nodes
        global _inductor_kernel_stack_trace
        global _inductor_triton_kernel_to_post_grad_node_info

        post_to_pre = _inductor_post_to_pre_grad_nodes.get("postToPre", {})
        all_kernels = OrderedSet(_inductor_kernel_stack_trace.keys()) | OrderedSet(
            _inductor_triton_kernel_to_post_grad_node_info.keys()
        )

        result = {}
        for kernel_name in all_kernels:
            post_grad_nodes = _inductor_triton_kernel_to_post_grad_node_info.get(
                kernel_name, []
            )

            pre_grad_nodes: OrderedSet[str] = OrderedSet()
            for post_node in post_grad_nodes:
                pre_grad_nodes.update(post_to_pre.get(post_node, []))

            result[kernel_name] = {
                "stack_traces": _inductor_kernel_stack_trace.get(kernel_name, []),
                "post_grad_nodes": post_grad_nodes,
                "pre_grad_nodes": list(pre_grad_nodes),
            }

        return result
    except Exception as e:
        signpost_event(
            "inductor",
            "provenance_tracking_error",
            {
                "function": "create_kernel_information_json",
                "error_msg": str(e),
                "stack_trace": traceback.format_exc(),
            },
        )
        return {}

