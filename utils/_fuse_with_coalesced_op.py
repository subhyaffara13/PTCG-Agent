
def _fuse_with_coalesced_op(
    graph: fx.Graph,
    last_input_node: fx.Node,
    all_input_nodes: list[fx.Node],
    last_comm_block: CommBlock,
) -> CommBlock:
    """Given a list of inputs in order, create a fused allreduce by coalesced."""
    last_comm_node = last_comm_block.comm_node
    last_wait_node = last_comm_block.wait_nodes[0]

    # Insert the fused div node and remove the input div nodes.
    # This is an optimization and is not mandatory for fusion.
    dividends = [div.args[0] for div in all_input_nodes]
    divisors = [div.args[1] for div in all_input_nodes]
    assert all(divisor == divisors[0] for divisor in divisors)
    with graph.inserting_before(last_input_node):
        last_input_node = call_function(
            graph, aten._foreach_div.Scalar, (dividends, divisors[0])
        )
    input_node = last_input_node

    # Create a new Comm/all_reduce_coalesced node.
    with graph.inserting_after(last_comm_node):
        flatten_args, spec = tree_flatten((last_comm_node.args, last_comm_node.kwargs))
        flatten_args[0] = input_node
        args, kwargs = tree_unflatten(flatten_args, spec)
        fused_comm_node = call_function(
            graph, torch.ops._c10d_functional.all_reduce_coalesced.default, args, kwargs
        )

    # Create a new wait node.
    getitem_nodes = []
    wait_nodes = []
    flatten_args, spec = tree_flatten((last_wait_node.args, last_wait_node.kwargs))
    for idx in range(len(all_input_nodes)):
        with graph.inserting_after(fused_comm_node):
            gi_node = call_function(graph, operator.getitem, (fused_comm_node, idx))
        getitem_nodes.append(gi_node)
        flatten_args[0] = gi_node
        args, kwargs = tree_unflatten(flatten_args, spec)
        with graph.inserting_after(gi_node):
            wait_nodes.append(call_function(graph, last_wait_node.target, args, kwargs))

    # Move the new all_reduce_coalesced and its args to right after the input node
    nodes_to_move = [fused_comm_node] + getitem_nodes + wait_nodes
    move_block_after(nodes_to_move, last_input_node)

    return CommBlock(
        shape=[
            tm.shape
            for tm in cast(
                list[TensorMetadata], fused_comm_node.meta.get("tensor_meta")
            )
        ],
        node_list=[fused_comm_node] + getitem_nodes + wait_nodes,
        wait_nodes=wait_nodes,
        comm_node=fused_comm_node,
        inputs=[input_node],
        outputs=OrderedSet(wait_nodes),
    )

