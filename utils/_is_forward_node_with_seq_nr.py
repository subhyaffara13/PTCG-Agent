
def _is_forward_node_with_seq_nr(node: torch.fx.Node) -> bool:
    # For now, assume that if nn_module_stack_metadata is populated, this
    # node is from the forward. Ignore nodes without `seq_nr`.
    # TODO(future): there is likely a less brittle way to do this by walking
    # the descendants of graph inputs corresponding to fwd inputs, didn't
    # seem obvious at first glance on how to partition graph inputs into
    # fwd vs bwd without relying on string names.
    return node.meta.get("partitioner_tag") != "is_backward" and "seq_nr" in node.meta

