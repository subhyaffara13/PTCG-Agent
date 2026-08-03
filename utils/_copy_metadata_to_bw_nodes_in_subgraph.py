import copy

def _copy_metadata_to_bw_nodes_in_subgraph(
    fx_g: torch.fx.GraphModule, fwd_seq_nr_to_node: dict[str, torch.fx.Node]
) -> None:
    """Copy metadata from forward nodes to backward nodes in a single subgraph."""
    for node in fx_g.graph.nodes:
        annotation_log.debug("node: %s", node.name)
        seq_nr = node.meta.get("seq_nr")
        annotation_log.debug("seq_nr: %s", seq_nr)

        if not _is_backward_node_with_seq_nr(node):
            continue

        # We exclude gradient accumulation nodes from copying tags
        if node.meta.get("is_gradient_acc", False):
            annotation_log.debug("is_gradient_acc")
            continue

        # fwd_node should always exist, but handle non-existence just in case
        fwd_node = fwd_seq_nr_to_node.get(node.meta["seq_nr"])
        if fwd_node is not None:
            node.meta["fwd_nn_module_stack"] = fwd_node.meta.get("nn_module_stack")
            node.meta["fwd_source_fn_stack"] = fwd_node.meta.get("source_fn_stack")
            # TODO: better to change to a specific field of custom?
            custom = fwd_node.meta.get("custom")
            if custom is not None:
                node.meta["custom"] = copy.deepcopy(custom)

