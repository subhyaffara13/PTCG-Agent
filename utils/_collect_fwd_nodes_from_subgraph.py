
def _collect_fwd_nodes_from_subgraph(
    fx_g: torch.fx.GraphModule, fwd_seq_nr_to_node: dict[str, torch.fx.Node]
) -> None:
    """Collect forward nodes from a single subgraph into the global mapping."""
    for node in fx_g.graph.nodes:
        if not _is_forward_node_with_seq_nr(node):
            continue
        seq_nr = node.meta["seq_nr"]
        if seq_nr in fwd_seq_nr_to_node:
            # If we already saw an op with the current `seq_nr`, that means
            # that the current op did not create an autograd node, and there
            # is no corresponding backward node, so we skip.
            continue
        fwd_seq_nr_to_node[seq_nr] = node

