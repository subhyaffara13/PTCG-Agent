
def _insert_copy_for_mutations(
    gm: torch.fx.GraphModule,
    mutated_outputs: Sequence[str | None],
    unlifted_name_to_node: dict[str, torch.fx.Node],
    input_name_to_node: dict[str, torch.fx.Node],
) -> None:
    """
    Find the all the buffers and inputs that were mutated and insert copy_
    operators to reflect mutations.
    """
    output_node = gm.graph.output_node()
    outputs = pytree.tree_flatten(output_node.args)[0]
    if len(outputs) != len(mutated_outputs):
        raise AssertionError(
            f"Number of outputs ({len(outputs)}) does not match "
            f"mutated outputs ({len(mutated_outputs)})"
        )

    user_output_nodes = []
    return_nodes_to_copy = {}
    for return_node, mutated_node_name in zip(outputs, mutated_outputs):
        if mutated_node_name is None:
            user_output_nodes.append(return_node)
            continue

        if mutated_node_name in unlifted_name_to_node:
            mutated_node = unlifted_name_to_node[mutated_node_name]
        elif mutated_node_name in input_name_to_node:
            mutated_node = input_name_to_node[mutated_node_name]
        else:
            raise RuntimeError(
                f"Could not find {mutated_node_name} in either buffer or input nodes"
            )

        with gm.graph.inserting_before(output_node):
            copy_node = gm.graph.call_function(
                torch.ops.aten.copy_.default, (mutated_node, return_node)
            )
            return_nodes_to_copy[return_node] = copy_node

    output_args = tuple(
        return_nodes_to_copy.get(node, node) for node in user_output_nodes
    )
    with gm.graph.inserting_before(output_node):
        # Only return user outputs
        new_output = gm.graph.output(output_args)
        output_node.replace_all_uses_with(new_output)
        gm.graph.erase_node(output_node)
        new_output.name = output_node.name
        new_output.meta.update(output_node.meta)
        new_output.meta["from_node"] = [
            NodeSource(
                output_node,
                "ExportedProgram.module().unlift()",
                [NodeSourceAction.CREATE, NodeSourceAction.REPLACE],
            )
        ]

