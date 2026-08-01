
def offload_activation_fw(graph: fx.Graph) -> None:
    """
    Insert CPU offload operations in the forward pass graph.

    Offload operations are placed after the last effective use of each tensor marked
    for offloading. This ensures the tensor is no longer needed on the GPU before
    transferring it to CPU memory.

    NOTE: An alternative approach would offload tensors immediately after generation
    to maximize compute-communication overlap. However, this requires additional
    synchronization to ensure tensor deletion (which occurs on the default stream)
    waits for the asynchronous offload operation to complete. This would necessitate
    more complex tracking to separate operation scheduling from memory cleanup.

    Args:
        graph: The forward graph to modify
    """

    op_types: OpTypes = get_default_op_list()

    output_node: fx.Node = graph.find_nodes(op="output")[0]
    # pyrefly: ignore [bad-assignment]
    fwd_outputs: tuple[fx.Node, ...] = output_node.args[
        0
    ]  # pyrefly: ignore [bad-assignment]
    node_to_offload: dict[fx.Node, fx.Node] = dict()
    node_to_index: dict[fx.Node, int] = {
        node: idx for idx, node in enumerate(graph.nodes)
    }

    for node in fwd_outputs:
        if node.meta.get("saved_for_offloading", False) is False:
            continue

        # Find insertion point, which is the last use
        if all_effective_users := _find_all_effective_users(node, op_types):
            last_user = max(all_effective_users, key=lambda n: node_to_index[n])
        else:
            last_user: fx.Node = node

        # Insert the CPU offload operation after the last user
        with graph.inserting_after(last_user):
            cpu_node: fx.Node = graph.call_function(
                torch.ops.prims.device_put.default,
                args=(node, torch.device("cpu")),
                kwargs={"non_blocking": True},
                name=CPU_OFFLOAD_PREFIX + str(node.name),
            )
            cpu_node.meta["val"] = node.meta["val"].to(torch.device("cpu"))
            cpu_node.meta["tensor_meta"] = extract_tensor_metadata(cpu_node.meta["val"])

        node_to_offload[node] = cpu_node

    # Update the return node args
    output_node.update_arg(
        0, tuple(node_to_offload.get(node, node) for node in fwd_outputs)
    )

