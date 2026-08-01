
def _handle_placeholder_node(
    node: torch.fx.Node,
    node_name_to_values: dict[str, ir.Value | Sequence[ir.Value]],
    *,
    graph_like: ir.Graph | ir.Function,
    lower: str,
    opset: onnxscript.values.Opset,
) -> None:
    # Placeholder nodes are user inputs
    # We need to create a new tensor for each user input
    # and add it to the graph's inputs
    name = node.name
    input_ = _tensors.SymbolicTensor(opset, name=name)
    input_.meta["node"] = node
    _set_shape_type(input_, node.meta["val"], complex_to_float=lower != "none")
    node_name_to_values[name] = input_
    # The inputs should be add to the graph here
    graph_like.inputs.append(input_)

