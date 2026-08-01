
def convert_conv_weights_to_channels_last(gm: torch.fx.GraphModule):
    """
    Convert 4d convolution weight tensor to channels last format.

    This pass is performed before freezing so the added nodes can be constant
    folded by freezing.
    """
    with dynamo_timed("convert_conv_weights_to_channels_last"):
        convs = [n for n in gm.graph.nodes if n.target is aten.convolution.default]
        for conv in convs:
            weight_node = conv.args[1]
            if len(weight_node.meta["val"].size()) != 4 or weight_node.meta[
                "val"
            ].is_contiguous(memory_format=torch.channels_last):
                # not a 4d tensor or already channels last, skip
                continue

            with gm.graph.inserting_before(conv):
                new_node = gm.graph.call_function(
                    aten.clone.default,
                    (weight_node,),
                    {"memory_format": torch.channels_last},
                )
                conv.replace_input_with(weight_node, new_node)

        enforce_as_strided_input_layout(gm)
        enforce_output_layout(gm)

