
def recover_original_precision_folded_computation_ops(gm):
    """
    After binary folding conv/linear weights and biases to a higher dtype, recover the original precision they were in.
    """
    graph = gm.graph
    for target, idx in (
        (aten.convolution.default, (1, 2)),
        (aten.addmm.default, (0, 2)),
        (aten.mm.default, (1,)),
    ):
        for node in graph.find_nodes(op="call_function", target=target):
            orig_dtype = node.meta.get("_allow_mixed_dtype_folding", None)
            if orig_dtype is None:
                continue

            with graph.inserting_before(node):
                for i in idx:
                    old_input = node.args[i]
                    if old_input is None:
                        continue

                    new_input = graph.create_node(
                        "call_function",
                        prims.convert_element_type.default,
                        (old_input, orig_dtype),
                    )
                    node.replace_input_with(old_input, new_input)

