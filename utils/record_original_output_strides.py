
def record_original_output_strides(gm: GraphModule) -> None:
    output_node = gm.graph.find_nodes(op="output")[0]
    output_strides = []

    if not isinstance(output_node.args[0], torch.fx.Node):
        output_node_args = output_node.args[0]
    else:
        output_node_args = output_node.args

    for output in output_node_args:
        if (
            isinstance(output, torch.fx.Node)
            and (val := output.meta.get("val")) is not None
            and isinstance(val, torch.Tensor)
        ):
            output_strides.append(val.stride())
        else:
            # pyrefly: ignore [bad-argument-type]
            output_strides.append(None)
    output_node.meta["original_output_strides"] = output_strides

