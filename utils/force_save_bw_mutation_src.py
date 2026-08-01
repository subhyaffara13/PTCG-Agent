
def force_save_bw_mutation_src(joint_module: fx.GraphModule) -> None:
    # If we have mutations of the same primal in forward and backward,
    # We must not recompute the source of mutation to not apply twice.
    has_mutation_in_bw: OrderedSet[torch.fx.Node] = OrderedSet()
    for node in reversed(joint_module.graph.nodes):
        if node.op == "output":
            continue

        is_copy_ = node.target is torch.ops.aten.copy_.default
        if is_copy_:
            if _has_tag_must_be_in_backward(node):
                has_mutation_in_bw.add(node.args[0])

            if _has_tag_must_be_in_forward(node) and node.args[0] in has_mutation_in_bw:
                node.args[1].meta["recompute"] = CheckpointPolicy.MUST_SAVE
        else:
            # We use invariant of aotdispatch joint graph,
            # That we emit copy_ only in the end of it.
            # We do not want to iterate through all the joint graph,
            # so break at the first non-output, non-copy_ node.
            break

