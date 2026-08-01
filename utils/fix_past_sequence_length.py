
def fix_past_sequence_length(model: OnnxModel):
    # Modify total_sequence_length = past_sequence_length + curr_sequence_length subgraph to calculate
    # past_sequence_length from the new `past_sequence_length` input of size 1D and type int32 instead of
    # from `past_key_self_0` since DecoderMaskedMultiHeadAttention (DMMHA) uses buffer sharing and
    # `past_key_self_0.shape[2] = max_sequence_length` instead of `past_key_self_0.shape[2] = past_sequence_length`
    # when buffer sharing is enabled
    #
    # Before:
    #
    #   input_ids      past_key_self_0
    #       |                 |
    #     Shape             Shape
    #       |                 |
    #     Gather            Gather
    #     (idx=1)           (idx=2)
    #       |                 |    \
    #       +--------+--------+    Unsqueeze
    #                |
    #               Add
    #
    # After:
    #
    #   input_ids    past_sequence_length (1D)
    #       |                 |
    #     Shape            Squeeze
    #       |                 |
    #     Gather             Cast
    #     (idx=1)           (int64)
    #       |                 |    \
    #       +--------+--------+    Unsqueeze
    #                |
    #               Add

    # Constant names to be used
    past_seq_len_name = "past_sequence_length"
    past_seq_len_int32 = "past_seq_len_int32"
    past_seq_len_int64 = "past_seq_len_int64"

    node = list(filter(lambda n: n.op_type == "LayerNormalization", model.model.graph.node))[0]  # noqa: RUF015

    base_path_hf = model.match_parent_path(
        node,
        ["Add", "Gather", "Tile", "Expand", "Unsqueeze", "Range"],
        [0, 1, 1, 0, 0, 0],
    )
    base_path_oai = model.match_parent_path(
        node,
        ["Add", "Slice"],
        [0, 1],
    )
    if base_path_hf is not None:
        base_path = base_path_hf
    elif base_path_oai is not None:
        base_path = base_path_oai
    else:
        logger.info("Cannot identify base path for fixing past_sequence_length subgraph")
        return
    base_node = base_path[-1]

    if base_node.op_type == "Range":
        # Hugging Face implementation
        range_node = base_path[-1]

        gather_path = model.match_parent_path(
            range_node,
            ["Gather", "Shape"],
            [0, 0],
        )
        if gather_path is None:
            logger.info("Cannot identify gather path for fixing past_sequence_length subgraph")
            return

        add_path = model.match_parent_path(
            range_node,
            ["Add", "Gather", "Shape"],
            [1, 0, 0],
        )
        if add_path is None:
            logger.info("Cannot identify add path for fixing past_sequence_length subgraph")
            return
        add_node = add_path[0]

        if gather_path != add_path[1:]:
            logger.info("Gather path and add path do not share the same nodes for calculating the past_sequence_length")
            return

        # Remove `past_key_self_0 --> Shape --> Gather` connection
        constant_in_gather = list(filter(lambda n: n.output[0] == gather_path[0].input[1], model.model.graph.node))[0]  # noqa: RUF015
        model.model.graph.node.remove(constant_in_gather)
        model.model.graph.node.remove(gather_path[0])
        model.model.graph.node.remove(gather_path[1])

        # Add `past_seq_len_int64` as an input name to existing nodes
        range_node.input[0] = past_seq_len_int64
        add_node.input[0] = past_seq_len_int64

    else:
        # OpenAI implementation
        input_ids_path = model.match_parent_path(
            base_node,
            ["Unsqueeze", "Add", "Gather", "Shape", "Reshape", "Transpose"],
            [2, 0, 0, 0, 0, 0],
        )
        if input_ids_path is None:
            logger.info("Cannot identify input_ids path for fixing past_sequence_length subgraph")
            return
        add_node = input_ids_path[1]

        past_key_path = model.match_parent_path(
            base_node,
            ["Unsqueeze", "Gather", "Shape", "Reshape", "Transpose"],
            [1, 0, 0, 0, 0],
        )
        if past_key_path is None:
            logger.info("Cannot identify past_key path for fixing past_sequence_length subgraph")
            return
        unsqueeze_node = past_key_path[0]

        if input_ids_path[2:] != past_key_path[1:]:
            logger.info(
                "The input_ids path and past_key path do not share the same nodes for calculating the past_sequence_length"
            )
            return

        # Remove `past_key_self_0 --> Transpose --> Reshape --> Shape --> Gather` connection
        constant_in_gather = list(filter(lambda n: n.output[0] == past_key_path[1].input[1], model.model.graph.node))[0]  # noqa: RUF015
        model.model.graph.node.remove(constant_in_gather)
        constant_in_reshape = list(filter(lambda n: n.output[0] == past_key_path[-2].input[1], model.model.graph.node))[  # noqa: RUF015
            0
        ]
        model.model.graph.node.remove(constant_in_reshape)
        model.model.graph.node.remove(past_key_path[1])
        model.model.graph.node.remove(past_key_path[2])
        model.model.graph.node.remove(past_key_path[3])
        model.model.graph.node.remove(past_key_path[4])

        # Add `past_seq_len_int64` as an input name to existing nodes
        unsqueeze_node.input[0] = past_seq_len_int64
        add_node.input[0] = past_seq_len_int64

    # Add `past_sequence_length` as model input
    model.model.graph.input.append(
        onnx.helper.make_tensor_value_info(past_seq_len_name, TensorProto.INT32, shape=[1]),
    )

    # Add `past_sequence_length --> Squeeze --> Cast` connection
    squeeze_node = onnx.helper.make_node(
        "Squeeze",
        inputs=[past_seq_len_name],
        outputs=[past_seq_len_int32],
        name=model.create_node_name("Squeeze"),
    )
    squeeze_output = onnx.helper.make_tensor_value_info(past_seq_len_int32, TensorProto.INT32, shape=[])
    cast_node = onnx.helper.make_node(
        "Cast",
        inputs=[past_seq_len_int32],
        outputs=[past_seq_len_int64],
        name=model.create_node_name("Cast"),
        to=TensorProto.INT64,
    )
    cast_output = onnx.helper.make_tensor_value_info(past_seq_len_int64, TensorProto.INT64, shape=[])

    # Add new nodes to graph
    model.model.graph.node.extend([squeeze_node, cast_node])
    model.model.graph.value_info.extend([squeeze_output, cast_output])
    model.topological_sort()
    return model, past_seq_len_name

