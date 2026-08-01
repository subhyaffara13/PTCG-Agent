
def _fuse_ddp_communication(
    graph: fx.Graph, algorithm_fn: Callable[..., Any], fusion_fn: Callable[..., Any]
) -> None:
    for output in reversed(graph.nodes):
        if output.op == "output":
            break

    def ddp_reducer_filter(block: CommBlock) -> bool:
        if (
            not isinstance(block.comm_node.args[0], fx.Node)
            or block.comm_node.args[0].target != aten.div.Tensor
        ):
            return False

        if len(block.wait_nodes[0].users) != 1:
            # gradient/wait node should only be used by one user
            return False

        # Two cases:
        # 1. gradient/wait node should be directly used by the output
        # if gradient is None before bwd.
        # 2. gradient/wait node should be directly used by copy_.
        if (
            output not in block.wait_nodes[0].users
            and next(iter(block.wait_nodes[0].users)).target != aten.copy_.default
        ):
            return False

        return True

    ops = (
        torch.ops._c10d_functional.all_reduce_.default,
        torch.ops._c10d_functional.all_reduce.default,
    )
    comm_blocks = get_all_comm_blocks(graph, ops, comm_filter=ddp_reducer_filter)
    node_indices = {node: i for i, node in enumerate(graph.nodes)}

    for block in algorithm_fn(graph, comm_blocks):
        fusion_fn(graph, block, node_indices)

