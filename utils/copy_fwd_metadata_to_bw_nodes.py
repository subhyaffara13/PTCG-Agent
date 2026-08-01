
def copy_fwd_metadata_to_bw_nodes(fx_g: torch.fx.GraphModule) -> None:
    """
    Input: `fx_g` which contains the joint fwd+bwd FX graph created by
    aot_autograd.

    This function walks the graph and copies over metadata from forward nodes
    to backward nodes, using the `seq_nr` field as a one-to-many mapping
    from forward node to backward node. This metadata is useful for performance
    profiling and debugging.

    This function supports matching forward and backward nodes across different
    subgraphs (e.g., in recursive submodules from HOPs), enabling backward nodes
    in any submodule to match forward nodes in any submodule.
    """

    # Build a global mapping of seq_nr to forward nodes across all subgraphs
    fwd_seq_nr_to_node: dict[str, torch.fx.Node] = {}

    # First pass: collect all forward nodes from all subgraphs
    for submod in fx_g.modules():
        if isinstance(submod, torch.fx.GraphModule):
            _collect_fwd_nodes_from_subgraph(submod, fwd_seq_nr_to_node)

    if annotation_log.isEnabledFor(logging.DEBUG):
        for k, v in fwd_seq_nr_to_node.items():
            annotation_log.debug("forward:: key: %s, value: %s", k, v)

    # Second pass: copy metadata to backward nodes in all subgraphs
    # using the global forward mapping
    for submod in fx_g.modules():
        if isinstance(submod, torch.fx.GraphModule):
            _copy_metadata_to_bw_nodes_in_subgraph(submod, fwd_seq_nr_to_node)

