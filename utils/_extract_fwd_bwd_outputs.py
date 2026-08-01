
def _extract_fwd_bwd_outputs(
    joint_module: fx.GraphModule, *, num_fwd_outputs: int
) -> tuple[list[fx.Node], list[fx.Node], list[AOTOutput], list[AOTOutput]]:
    outputs = pytree.arg_tree_leaves(
        *(node.args for node in joint_module.graph.find_nodes(op="output"))
    )
    outputs_descs = pytree.arg_tree_leaves(
        next(iter(joint_module.graph.find_nodes(op="output"))).meta.get(
            "desc", [None] * len(outputs)
        )
    )
    fwd_outputs = outputs[:num_fwd_outputs]
    bwd_outputs = outputs[num_fwd_outputs:]
    fwd_outputs_descs = outputs_descs[:num_fwd_outputs]
    bwd_outputs_descs = outputs_descs[num_fwd_outputs:]
    return fwd_outputs, bwd_outputs, fwd_outputs_descs, bwd_outputs_descs

