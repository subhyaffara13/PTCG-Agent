
def _is_backward_node_with_seq_nr(node: torch.fx.Node) -> bool:
    # For now, assume that if nn_module_stack_metadata is not populated,
    # this node is from the backward. Ignore nodes without `seq_nr`.
    # TODO(future): there is likely a less brittle way to do this, same
    # as with the forward.
    return node.meta.get("partitioner_tag") == "is_backward" and "seq_nr" in node.meta

