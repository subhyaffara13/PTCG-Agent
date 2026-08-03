from typing import Any

def _get_seq_nr(node_name: str = "") -> int | None:
    """
    Returns the seq_nr node meta for the current proxy node that we're creating.
    The seq_nr number in node meta is related to but not the same as the "sequence number"
    in autograd.
    We use the seq_nr to correlate forward and backward nodes in the traced FX graphs
    (e.g. in copy_fwd_metadata_to_bw_nodes).
    The corresponding forward and backward FX graph nodes should have the same seq_nr.

    The ordering of the seq_nr in the graph does not indicate when the node is executed.
    For example, the nodes in the invoke_subgraph HOP's subgraph may be called multiple
    times by different HOP nodes, but these nodes only have a single seq_nr, which may be
    smaller, the same, or larger than the calling HOP.

    `node_name` is the name of the node that we're creating. It is used for logging only.
    """
    current_meta: dict[str, Any] = fx_traceback.get_current_meta()
    new_seq_nr = None
    # The sequence_nr increments every time a new autograd Node
    # is created. During the FWD pass we store the sequence_nr
    # corresponding to the last autograd Node created on this fx
    # node's meta.  A single aten op can create multiple autograd
    # nodes as is the case with in-place foreach ops. During the
    # BWD pass we retrieve the sequence_nr stored on the current
    # executing autograd Node. See NOTE [ Sequence Number ].
    if current_meta.get("in_grad_fn", 0) > 0:
        # This branch is used to get seq_nr for backward nodes
        annotation_log.debug("%s: seq_nr from current_meta grad_fn_seq_nr", node_name)
        new_seq_nr = current_meta["grad_fn_seq_nr"][-1]

    elif torch.fx.traceback._is_preserving_node_seq_nr():
        # Special case where we preserve seq_nr from currently tracing node
        # Used to preserve seq_nr when re-tracing subgraphs in HOP
        annotation_log.debug("%s: seq_nr from current_meta seq_nr", node_name)
        new_seq_nr = current_meta.get("seq_nr")
    else:
        # Here we decrement to account for the sequence_nr having
        # just been incremented while tracing this lowered aten op.
        # This branch is used to get seq_nr for forward nodes
        new_seq_nr = torch.autograd._get_sequence_nr() - 1

    if not torch.fx.traceback._is_preserving_node_seq_nr():
        # See Note [Functionalization View Replay Annotation]
        # Overriding some node meta with the original node meta of the
        # regenerated node.
        replay_node: Node | None = fx_traceback.get_current_replay_node()
        if replay_node is not None:
            if "seq_nr" in replay_node.meta:
                annotation_log.debug("%s: seq_nr from replay_node", node_name)
                new_seq_nr = replay_node.meta["seq_nr"]

    return new_seq_nr

