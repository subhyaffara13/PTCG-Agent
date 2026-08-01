
def _fuse_allreduce_by_concat(
    graph: fx.Graph,
    last_input_node: fx.Node,
    all_input_nodes: list[fx.Node],
    last_comm_block: CommBlock,
) -> CommBlock:
    """Given a list of inputs in order, create a fused allreduce using concat."""
    # Flatten all the inputs to the all_reduce nodes.
    with graph.inserting_after(last_input_node):
        cat_inputs = []
        for input_node in all_input_nodes:
            assert isinstance(input_node.args[0], fx.Node)
            input_node = input_node.args[0]
            cat_inputs.append(
                call_function(graph, aten.flatten.using_ints, (input_node,))
            )

    # Concat all the flattened nodes.
    with graph.inserting_after(cat_inputs[0]):
        cat_node = call_function(graph, aten.cat, (cat_inputs,))

    # Insert the fused div node and remove the input div nodes.
    # This is an optimization and is not mandatory for fusion.
    divisors = [div.args[1] for div in all_input_nodes]
    assert all(divisor == divisors[0] for divisor in divisors)
    with graph.inserting_after(cat_node):
        div_node = call_function(graph, last_input_node.target, (cat_node, divisors[0]))

    # Create a new Comm/all_reduce node.
    last_comm_node = last_comm_block.comm_node
    last_wait_node = last_comm_block.wait_nodes[0]
    with graph.inserting_after(div_node):
        flatten_args, spec = tree_flatten((last_comm_node.args, last_comm_node.kwargs))
        flatten_args[0] = div_node
        args, kwargs = tree_unflatten(flatten_args, spec)
        fused_comm_node = call_function(graph, last_comm_node.target, args, kwargs)

    # Create a new Wait node.
    with graph.inserting_after(fused_comm_node):
        flatten_args, spec = tree_flatten((last_wait_node.args, last_wait_node.kwargs))
        flatten_args[0] = fused_comm_node
        args, kwargs = tree_unflatten(flatten_args, spec)
        fused_wait_node = call_function(graph, last_wait_node.target, args, kwargs)

    # Move the fused all_reduce and its args to right after the input node
    nodes_to_move = cat_inputs + [cat_node, div_node, fused_comm_node, fused_wait_node]
    # pyrefly: ignore [bad-argument-type]
    move_block_after(nodes_to_move, last_input_node)

    return CommBlock(
        shape=cast(TensorMetadata, cat_node.meta.get("tensor_meta")).shape,
        node_list=[fused_comm_node, fused_wait_node],
        wait_nodes=[fused_wait_node],
        comm_node=fused_comm_node,
        inputs=[div_node],
        outputs=OrderedSet([fused_wait_node]),
    )

