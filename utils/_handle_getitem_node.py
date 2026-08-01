
def _handle_getitem_node(
    node: torch.fx.Node, node_name_to_values: dict[str, ir.Value | Sequence[ir.Value]]
) -> ir.Value:
    """Handle a getitem node.

    Add the input value it is getting to the mapping, then return the value.

    There are two cases for this node:
    1. The output is a Sequence (traced), we can simply get the value from the sequence
    2. The output is produced by a SplitToSequence node, we need to get the value from the sequence value
    This function only handles the first case
    """
    if len(node.all_input_nodes) != 1:
        raise AssertionError(f"Expected 1 input node, got {len(node.all_input_nodes)}")
    source = node.all_input_nodes[0]
    source_outputs = node_name_to_values[source.name]
    if not isinstance(source_outputs, Sequence):
        raise AssertionError(
            f"Expected {source.name} to output sequence, got {node_name_to_values[source.name]}"
        )
    index = typing.cast(int, node.args[1])
    value = source_outputs[index]
    # Save the getitem value to the values mapping to in case
    # it is one of the graph outputs
    node_name_to_values[node.name] = value
    # Rename the name of value with the getitem name.
    value.name = node.name
    return value

