
def force_save_effectful_ops(joint_module: fx.GraphModule) -> None:
    """
    Force save outputs from with_effects nodes wrapping effectful ops.

    Effectful ops (registered via _register_effectful_op) should not be recomputed
    because they may have arbitrary global side effects (I/O, RNG state, collectives,
    etc.). We mark the tensor outputs of with_effects as MUST_SAVE to prevent
    recomputation of the effectful op.

    The with_effects node returns a tuple (token, result). We recursively find all
    leaf outputs extracted via getitem and mark them as MUST_SAVE. Since these are
    saved, the with_effects op doesn't need to be recomputed in backward.
    """

    def mark_getitem_outputs(node: fx.Node) -> None:
        for user in node.users:
            if user.target is operator.getitem:
                mark_getitem_outputs(user)
                if not isinstance(user.meta.get("val"), (tuple, list)):
                    user.meta["recompute"] = CheckpointPolicy.MUST_SAVE

    for node in joint_module.graph.nodes:
        if (
            is_with_effects(node)
            and not must_recompute(node)
            and not _has_tag_is_backward(node)
        ):
            mark_getitem_outputs(node)

