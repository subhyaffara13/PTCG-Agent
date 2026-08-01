
def force_save_collectives(joint_module: fx.GraphModule) -> None:
    """
    By default, the partitioner is not allowed to recompute collectives
    unless they come from a user-annotated AC region.
    See Note [Recomputing collectives in the partitioner]
    """
    for node in joint_module.graph.nodes:
        if (
            isinstance(node.target, torch._ops.OpOverload)
            and node.target.namespace == "_c10d_functional"
            and not must_recompute(node)
        ):
            node.meta["recompute"] = CheckpointPolicy.MUST_SAVE

