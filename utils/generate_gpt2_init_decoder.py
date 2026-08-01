
def generate_gpt2_init_decoder(
    decoder_onnx_path: str,
    init_decoder_onnx_path: str,
    use_external_data_format: bool = True,
) -> bool:
    """Generates the initial decoder GPT2 subgraph and saves it for downstream use.
       The initial decoder model will be saved to init_decoder_onnx_path.

    Args:
        decoder_onnx_path (str): Path of GPT-2 decoder onnx model
        init_decoder_onnx_path (str): Path of GPT-2 init decoder onnx model
        use_external_data_format(bool): output tensors to external data or not.
    """
    init_decoder_model_proto = onnx.load_model(decoder_onnx_path, load_external_data=True)

    logits_output_name = init_decoder_model_proto.graph.output[0].name

    gpt2_init_decoder_model = OnnxModel(init_decoder_model_proto)

    output_name_to_node = gpt2_init_decoder_model.output_name_to_node()
    assert logits_output_name in output_name_to_node

    logits_matmul_node = output_name_to_node[logits_output_name]

    # Sanity check - the logits need to be produced by a MatMul node
    if logits_matmul_node.op_type != "MatMul":
        return False

    # Try to find the last residual Add
    # For fp16, there are Casts along the way

    # Normalization Node is : LayerNormalization
    logits_matmul_to_residual_add_path = gpt2_init_decoder_model.match_parent_path(
        logits_matmul_node,
        [
            "Cast",
            "LayerNormalization",
            "Add",
            "Add",
            "Cast",
            "MatMul",
            "Cast",
            "FastGelu",
            "Cast",
            "MatMul",
            "Cast",
            "LayerNormalization",
            "Add",
        ],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )

    # Normalization Node is : SkipLayerNormalization
    if logits_matmul_to_residual_add_path is None:
        logits_matmul_to_residual_add_path = gpt2_init_decoder_model.match_parent_path(
            logits_matmul_node,
            [
                "Cast",
                "SkipLayerNormalization",
                "Cast",
                "MatMul",
                "Cast",
                "FastGelu",
                "Cast",
                "MatMul",
                "Cast",
                "SkipLayerNormalization",
            ],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        )

    # Try without the Casts before and after the MatMuls
    if logits_matmul_to_residual_add_path is None:
        # Normalization Node is : LayerNormalization
        logits_matmul_to_residual_add_path = gpt2_init_decoder_model.match_parent_path(
            logits_matmul_node,
            [
                "LayerNormalization",
                "Add",
                "Add",
                "MatMul",
                "FastGelu",
                "MatMul",
                "LayerNormalization",
                "Add",
            ],
            [0, 0, 1, 0, 0, 0, 0, 0],
        )

        # Normalization Node is : SkipLayerNormalization
        if logits_matmul_to_residual_add_path is None:
            logits_matmul_to_residual_add_path = gpt2_init_decoder_model.match_parent_path(
                logits_matmul_node,
                [
                    "SkipLayerNormalization",
                    "MatMul",
                    "FastGelu",
                    "MatMul",
                    "SkipLayerNormalization",
                ],
                [0, 1, 0, 0, 0],
            )

    # TODO(hasesh): Are there more permutations to try before returning ?
    if logits_matmul_to_residual_add_path is None:
        return False

    residual_add_node = logits_matmul_to_residual_add_path[-1]

    # If the last node in the pattern is SkipLayerNormalization, we need to adjust our pattern searches accordingly
    is_skiplayernorm_path = residual_add_node.op_type == "SkipLayerNormalization"

    # Regular LayerNormalization path
    if not is_skiplayernorm_path:
        residual_add_to_attention_parent_index = 0
        residual_add_to_attention_path = gpt2_init_decoder_model.match_parent_path(
            residual_add_node,
            ["Add", "Cast", "MatMul", "Attention"],
            [residual_add_to_attention_parent_index, 0, 0, 0],
        )

        # Try other parent index of the residual Add node
        if residual_add_to_attention_path is None:
            residual_add_to_attention_parent_index = 1
            residual_add_to_attention_path = gpt2_init_decoder_model.match_parent_path(
                residual_add_node,
                ["Add", "Cast", "MatMul", "Attention"],
                [residual_add_to_attention_parent_index, 0, 0, 0],
            )

        # Try without the Casts before and after the MatMuls
        if residual_add_to_attention_path is None:
            residual_add_to_attention_parent_index = 0
            residual_add_to_attention_path = gpt2_init_decoder_model.match_parent_path(
                residual_add_node,
                ["Add", "MatMul", "Attention"],
                [residual_add_to_attention_parent_index, 0, 0],
            )

        # Try without the Casts before and after the MatMuls and other parent index of the residual Add node
        if residual_add_to_attention_path is None:
            residual_add_to_attention_parent_index = 1
            residual_add_to_attention_path = gpt2_init_decoder_model.match_parent_path(
                residual_add_node,
                ["Add", "MatMul", "Attention"],
                [residual_add_to_attention_parent_index, 0, 0],
            )

    # SkipLayerNormalization path
    else:
        residual_add_to_attention_parent_index = 0
        residual_add_to_attention_path = gpt2_init_decoder_model.match_parent_path(
            residual_add_node,
            ["Cast", "MatMul", "Attention"],
            [residual_add_to_attention_parent_index, 0, 0],
        )

        # Try other parent index of the residual Add node
        if residual_add_to_attention_path is None:
            residual_add_to_attention_parent_index = 1
            residual_add_to_attention_path = gpt2_init_decoder_model.match_parent_path(
                residual_add_node,
                ["Cast", "MatMul", "Attention"],
                [residual_add_to_attention_parent_index, 0, 0],
            )

        # Try without the Casts before and after the MatMuls
        if residual_add_to_attention_path is None:
            residual_add_to_attention_parent_index = 0
            residual_add_to_attention_path = gpt2_init_decoder_model.match_parent_path(
                residual_add_node,
                ["MatMul", "Attention"],
                [residual_add_to_attention_parent_index, 0],
            )

        # Try without the Casts before and after the MatMuls and other parent index of the residual Add node
        if residual_add_to_attention_path is None:
            residual_add_to_attention_parent_index = 1
            residual_add_to_attention_path = gpt2_init_decoder_model.match_parent_path(
                residual_add_node,
                ["MatMul", "Attention"],
                [residual_add_to_attention_parent_index, 0],
            )

    # TODO(hasesh): Are there more permutations to try before returning ?
    if residual_add_to_attention_path is None:
        return False

    residual_add_to_add_parent_index = 0 if residual_add_to_attention_parent_index == 1 else 1

    # Regular LayerNormalization path
    if not is_skiplayernorm_path:
        add_before_residual_add = gpt2_init_decoder_model.match_parent(
            residual_add_node, "Add", residual_add_to_add_parent_index
        )

    # SkipLayerNormalization path
    else:
        add_before_residual_add = gpt2_init_decoder_model.match_parent(
            residual_add_node,
            "SkipLayerNormalization",
            residual_add_to_add_parent_index,
        )

    if add_before_residual_add is None:
        return False

    attention = residual_add_to_attention_path[-1]
    matmul_after_attention = residual_add_to_attention_path[-2]

    slice_starts = onnx.helper.make_tensor(
        name="SliceLastTokenStarts",
        data_type=TensorProto.INT32,
        dims=[1],
        vals=[-1],
    )

    slice_ends = onnx.helper.make_tensor(
        name="SliceLastTokenEnds",
        data_type=TensorProto.INT32,
        dims=[1],
        vals=[-2],
    )

    slice_axes = onnx.helper.make_tensor(
        name="SliceLastTokenAxes",
        data_type=TensorProto.INT32,
        dims=[1],
        vals=[1],
    )

    slice_steps = onnx.helper.make_tensor(
        name="SliceLastTokenSteps",
        data_type=TensorProto.INT32,
        dims=[1],
        vals=[-1],
    )

    gpt2_init_decoder_model.add_initializer(slice_starts)
    gpt2_init_decoder_model.add_initializer(slice_ends)
    gpt2_init_decoder_model.add_initializer(slice_axes)
    gpt2_init_decoder_model.add_initializer(slice_steps)

    # Add Slice node to the graph such that it consumes the output of Attention
    slice_0_output_name = "edge_modified_" + attention.output[0]
    slice_node_0 = onnx.helper.make_node(
        "Slice",
        inputs=[
            attention.output[0],
            "SliceLastTokenStarts",
            "SliceLastTokenEnds",
            "SliceLastTokenAxes",
            "SliceLastTokenSteps",
        ],
        outputs=[slice_0_output_name],
        name=gpt2_init_decoder_model.create_node_name("Slice", "GatherLastToken_0_"),
    )

    # Add Slice node to the graph such that it consumes the output of Add before the residual Add
    # If the 'Add' output is produced by a SkipLayerNormalization node, then adjust its output
    # index appropriately
    add_before_residual_add_output = (
        add_before_residual_add.output[0] if not is_skiplayernorm_path else add_before_residual_add.output[3]
    )

    slice_1_output_name = "edge_modified_" + add_before_residual_add.output[0]
    slice_node_1 = onnx.helper.make_node(
        "Slice",
        inputs=[
            add_before_residual_add_output,
            "SliceLastTokenStarts",
            "SliceLastTokenEnds",
            "SliceLastTokenAxes",
            "SliceLastTokenSteps",
        ],
        outputs=[slice_1_output_name],
        name=gpt2_init_decoder_model.create_node_name("Slice", "GatherLastToken_1_"),
    )

    # Add the 2 Slice nodes
    gpt2_init_decoder_model.add_node(slice_node_0)
    gpt2_init_decoder_model.add_node(slice_node_1)

    # Adjust the input(s) to the nodes consuming the outputs of the added Slice nodes
    gpt2_init_decoder_model.replace_node_input(matmul_after_attention, attention.output[0], slice_0_output_name)
    gpt2_init_decoder_model.replace_node_input(residual_add_node, add_before_residual_add_output, slice_1_output_name)

    # Topologically sort the updated graph
    gpt2_init_decoder_model.topological_sort()

    # Save the init decoder model
    OnnxModel.save(
        init_decoder_model_proto,
        init_decoder_onnx_path,
        save_as_external_data=use_external_data_format,
    )
    return True

