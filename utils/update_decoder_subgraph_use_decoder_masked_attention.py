
def update_decoder_subgraph_use_decoder_masked_attention(
    subg: GraphProto, is_beam_search: bool, switch_attention: bool
) -> bool:
    """Update the Attention nodes to DecoderMaskedSelfAttention.

    Args:
        subg (GraphProto): GraphProto of the decoder subgraph
        is_beam_search (bool): Boolean specifying if the sampling algo is BeamSearch
        switch_attention (bool): Boolean specifying if `Attention` is to be switched with `DecoderMaskedSelfAttention`
    """
    if is_beam_search:
        new_inputs = []
        for _i, vi in enumerate(subg.input):
            new_inputs.extend([vi])

        # Add 2 BeamSearch specific inputs
        new_inputs.extend([onnx.helper.make_tensor_value_info("beam_width", onnx.TensorProto.INT32, shape=[1])])
        new_inputs.extend(
            [
                onnx.helper.make_tensor_value_info(
                    "cache_indirection",
                    onnx.TensorProto.INT32,
                    shape=["batch_size", "beam_width", "max_seq_len"],
                )
            ]
        )
        subg.ClearField("input")
        subg.input.extend(new_inputs)

    if switch_attention:
        decoder_masked_attention_supported_attr = [
            "past_present_share_buffer",
            "num_heads",
            "scale",
            "mask_filter_value",
            "domain",
        ]

        new_nodes = []
        for node in subg.node:
            if node.op_type == "Attention":
                kwargs = kwargs_of(node)
                for k in kwargs.copy():
                    # The Attention operator does not support different qkv hidden sizes when past/present
                    # input/output exists (GPT2 model). Hence, we should never run into this.
                    # But, if we do, do not go ahead with the optimization.
                    if k == "qkv_hidden_sizes":
                        return False

                    if k not in decoder_masked_attention_supported_attr:
                        # Log the fact that we are removing certain attributes from the node
                        # We don't need to log it for "unidirectional" as we are aware that
                        # decoding attention kernels are unidirectional by definition.
                        if k != "unidirectional":
                            logger.warning(
                                f"Removing attribute: {k} from Attention node while switching to DecoderMaskedSelfAttention"
                            )

                        del kwargs[k]

                nis = []
                nis.extend(node.input)

                # Add 2 BeamSearch specific inputs
                if is_beam_search:
                    while len(nis) < 7:
                        nis.extend([""])
                    if len(nis) < 8:
                        nis.extend(["beam_width"])
                    if len(nis) < 9:
                        nis.extend(["cache_indirection"])

                node = onnx.helper.make_node(  # noqa: PLW2901
                    "DecoderMaskedSelfAttention",
                    nis,
                    node.output,
                    name=node.name,
                    **kwargs,
                )
            new_nodes.extend([node])
        subg.ClearField("node")
        subg.node.extend(new_nodes)

    return True

