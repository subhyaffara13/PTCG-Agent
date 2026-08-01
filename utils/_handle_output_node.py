
def _handle_output_node(
    node: torch.fx.Node,
    node_name_to_values: dict[str, ir.Value | Sequence[ir.Value]],
    graph_like: ir.Graph | ir.Function,
) -> None:
    """Handle an output node by adding the output to the graph's outputs.

    Args:
        node: The FX node to translate.
        node_name_to_values: A mapping of FX node names to their produced ONNX ``Value``.
        graph_like: The ONNX graph at construction.
    """
    if not isinstance(node.args[0], Sequence):
        output_nodes = (node.args[0],)
    else:
        # node.args[0] can be a tuple with more than one elements. This happens when,
        # for example, a subgraph has multiple outputs. We flatten them all as ONNX graph outputs
        output_nodes = node.args[0]
    for output in output_nodes:
        if output is None:
            logger.warning(
                "Output node %s has None output. The output is ignored in the exported graph. Please ensure the graph output order is expected",
                node.name,
            )
            continue
        output_value_name = output.name  # type: ignore[union-attr]
        if not isinstance(output_value_name, str):
            raise AssertionError(f"Bug: Expected {output_value_name!r} to be a string")
        values = node_name_to_values[output_value_name]
        if isinstance(values, Sequence):
            graph_like.outputs.extend(values)
            return
        graph_like.outputs.append(values)

