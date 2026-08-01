
def _unlift_inputs_as_getattr(
    gm: torch.fx.GraphModule,
    lifted_inputs: Sequence[str | None],
) -> tuple[dict[str, torch.fx.Node], dict[str, torch.fx.Node]]:
    """
    Unlift inputs referring to params/buffers/constants as getattr nodes in the
    graph
    """
    unlifted_name_to_node = {}
    input_name_to_node = {}

    placeholder_nodes = [node for node in gm.graph.nodes if node.op == "placeholder"]
    if len(lifted_inputs) != len(placeholder_nodes):
        raise AssertionError(
            f"Number of lifted inputs ({len(lifted_inputs)}) does not match "
            f"placeholder nodes ({len(placeholder_nodes)})"
        )
    for input_node, lifted_node in zip(placeholder_nodes, lifted_inputs):
        if lifted_node is None:
            input_name_to_node[input_node.name] = input_node

        else:
            with gm.graph.inserting_after(input_node):
                # It is fine to ignore this warning because
                # it is guaranteed that we will populate this
                # attr later.
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    getattr_node = gm.graph.get_attr(lifted_node)
                input_node.replace_all_uses_with(getattr_node)
                metadata = input_node.meta
                gm.graph.erase_node(input_node)
                getattr_node.meta = metadata
                getattr_node.meta["from_node"] = [
                    NodeSource(
                        input_node,
                        "ExportedProgram.module().unlift()",
                        [NodeSourceAction.CREATE, NodeSourceAction.REPLACE],
                    )
                ]
                unlifted_name_to_node[lifted_node] = getattr_node

    return unlifted_name_to_node, input_name_to_node

