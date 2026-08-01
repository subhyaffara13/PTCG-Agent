
def replace_mha_with_gqa(
    model: OnnxModel,
    attn_mask: str,
    kv_num_heads: int = 0,
    world_size: int = 1,
    window_size: int = -1,
):
    # Insert attention_mask subgraph to calculate shared inputs for all GroupQueryAttention nodes
    #
    #                attention_mask
    #               /              \
    #          ReduceSum          Shape
    #              |                |
    #             Sub             Gather
    #              |                |
    #          seqlens_k   total_sequence_length
    #              |                |
    #        Cast to int32    Cast to int32

    model.add_initializer(
        onnx.helper.make_tensor(
            name="one",
            data_type=TensorProto.INT64,
            dims=[1],
            vals=[1],
        )
    )
    reduce_sum_node = onnx.helper.make_node(
        "ReduceSum",
        inputs=[attn_mask, "one"],
        outputs=[attn_mask + "_row_sums"],
        name=model.create_node_name("ReduceSum"),
    )
    sub_node = onnx.helper.make_node(
        "Sub",
        inputs=[attn_mask + "_row_sums", "one"],
        outputs=["seqlens_k_int64"],
        name=model.create_node_name("Sub"),
    )
    seqlen_k_cast_node = onnx.helper.make_node(
        "Cast",
        inputs=["seqlens_k_int64"],
        outputs=["seqlens_k"],
        name=model.create_node_name("Cast"),
        to=TensorProto.INT32,
    )
    shape_node = onnx.helper.make_node(
        "Shape",
        inputs=[attn_mask],
        outputs=[attn_mask + "_shape"],
        name=model.create_node_name("Shape"),
    )
    gather_node = onnx.helper.make_node(
        "Gather",
        inputs=[attn_mask + "_shape", "one"],
        outputs=["total_seq_len_int64"],
        name=model.create_node_name("Gather"),
        axis=0,
    )
    total_seqlen_cast_node = onnx.helper.make_node(
        "Cast",
        inputs=["total_seq_len_int64"],
        outputs=["total_seq_len"],
        name=model.create_node_name("Cast"),
        to=TensorProto.INT32,
    )
    model.model.graph.node.extend(
        [
            reduce_sum_node,
            sub_node,
            seqlen_k_cast_node,
            shape_node,
            gather_node,
            total_seqlen_cast_node,
        ]
    )

    # Replace MultiHeadAttention with GroupQueryAttention
    #
    # When replacing, fuse the following subgraph:
    #
    #                 root_input
    #               /     |      \
    #         MatMul    MatMul    MatMul
    #           |         |         |
    #          Add       Add       Add      (optional Adds)
    #           |         |         |
    #         RotEmb    RotEmb      |
    #            \        |        /
    #             MultiHeadAttention
    #
    # to this new subgraph:
    #
    #                 root_input
    #                     |
    #                PackedMatMul           (if possible)
    #                     |
    #                 PackedAdd             (if possible)
    #                     |
    #             GroupQueryAttention
    #

    mha_nodes = list(filter(lambda node: node.op_type == "MultiHeadAttention", model.model.graph.node))
    for idx, node in enumerate(mha_nodes):
        # Detect Q path to MHA
        q_path_1 = model.match_parent_path(node, ["RotaryEmbedding", "Add", "MatMul"], [0, 0, 0])
        q_path_2 = model.match_parent_path(node, ["RotaryEmbedding", "MatMul"], [0, 0])

        q_rotary, q_add, q_matmul = None, None, None
        if q_path_1 is not None:
            q_rotary, q_add, q_matmul = q_path_1
        elif q_path_2 is not None:
            q_rotary, q_matmul = q_path_2

        # Detect K path to MHA
        k_path_1 = model.match_parent_path(node, ["RotaryEmbedding", "Add", "MatMul"], [1, 0, 0])
        k_path_2 = model.match_parent_path(node, ["RotaryEmbedding", "MatMul"], [1, 0])

        k_rotary, k_add, k_matmul = None, None, None
        if k_path_1 is not None:
            k_rotary, k_add, k_matmul = k_path_1
        elif k_path_2 is not None:
            k_rotary, k_matmul = k_path_2

        # Detect V path to MHA
        v_path_1 = model.match_parent_path(node, ["Add", "MatMul"], [2, 0])
        v_path_2 = model.match_parent_path(node, ["MatMul"], [2])

        v_add, v_matmul = None, None
        if v_path_1 is not None:
            v_add, v_matmul = v_path_1
        elif v_path_2 is not None:
            v_matmul = v_path_2[0]

        # Get `interleaved` attribute from RotaryEmbedding
        interleaved = 0
        if q_rotary is not None and k_rotary is not None:
            for att in q_rotary.attribute:
                if att.name == "interleaved":
                    interleaved = att.i

        # Get `num_heads` attribute from MHA
        num_heads = 0
        for att in node.attribute:
            if att.name == "num_heads":
                num_heads = att.i

        # Check if root_input to Q/K/V paths is the same
        root_input_is_same = q_matmul.input[0] == k_matmul.input[0] and k_matmul.input[0] == v_matmul.input[0]

        # Check if Q/K/V paths all have bias or all don't have bias
        all_paths_have_bias = q_add is not None and k_add is not None and v_add is not None
        all_paths_have_no_bias = q_add is None and k_add is None and v_add is None

        # Make PackedMatMul node if possible
        q_input_to_attention, k_input_to_attention, v_input_to_attention = "", "", ""
        if root_input_is_same and (all_paths_have_bias or all_paths_have_no_bias):
            qw = NumpyHelper.to_array(model.get_initializer(q_matmul.input[1]))
            kw = NumpyHelper.to_array(model.get_initializer(k_matmul.input[1]))
            vw = NumpyHelper.to_array(model.get_initializer(v_matmul.input[1]))

            dim = qw.shape[-1]
            qkv_weight = np.stack((qw, kw, vw), axis=1).reshape(dim, 3 * dim)
            qkv_weight = onnx.numpy_helper.from_array(qkv_weight, name=f"QKV_Weight_{idx}")
            model.add_initializer(qkv_weight)

            packed_matmul_node = onnx.helper.make_node(
                "MatMul",
                inputs=[q_matmul.input[0], qkv_weight.name],
                outputs=[f"{qkv_weight.name}_output"],
                name=model.create_node_name("MatMul"),
            )
            model.model.graph.node.extend([packed_matmul_node])
            model.model.graph.node.remove(q_matmul)
            model.model.graph.node.remove(k_matmul)
            model.model.graph.node.remove(v_matmul)
            q_input_to_attention = packed_matmul_node.output[0]

            # Make PackedAdd node if possible
            if all_paths_have_bias:
                qb = NumpyHelper.to_array(model.get_initializer(q_add.input[1]))
                kb = NumpyHelper.to_array(model.get_initializer(k_add.input[1]))
                vb = NumpyHelper.to_array(model.get_initializer(v_add.input[1]))

                dim = qb.shape[-1]
                qkv_bias = np.stack((qb, kb, vb), axis=0).reshape(3 * dim)
                qkv_bias = onnx.numpy_helper.from_array(qkv_bias, name=f"QKV_Bias_{idx}")
                model.add_initializer(qkv_bias)
                packed_add_node = onnx.helper.make_node(
                    "Add",
                    inputs=[packed_matmul_node.output[0], qkv_bias.name],
                    outputs=[f"{qkv_bias.name}_output"],
                )
                model.model.graph.node.extend([packed_add_node])
                model.model.graph.node.remove(q_add)
                model.model.graph.node.remove(k_add)
                model.model.graph.node.remove(v_add)
                q_input_to_attention = packed_add_node.output[0]

        else:
            q_input_to_attention = q_matmul.output[0]
            k_input_to_attention = k_matmul.output[0]
            v_input_to_attention = v_matmul.output[0]

        # Make GQA node
        gqa_node = onnx.helper.make_node(
            "GroupQueryAttention",
            inputs=[
                q_input_to_attention,  # query
                k_input_to_attention,  # key
                v_input_to_attention,  # value
                node.input[6],  # past_key
                node.input[7],  # past_value
                seqlen_k_cast_node.output[0],  # seqlens_k (for attention mask)
                total_seqlen_cast_node.output[0],  # total_seq_len (for attention mask)
                (q_rotary.input[2] if q_rotary is not None else ""),  # cos_cache (for rotary embeddings)
                (q_rotary.input[3] if q_rotary is not None else ""),  # sin_cache (for rotary embeddings)
            ],
            outputs=node.output,
            name=node.name.replace("MultiHeadAttention", "GroupQueryAttention"),
            domain="com.microsoft",
            num_heads=num_heads // world_size,
            kv_num_heads=(num_heads // world_size if kv_num_heads == 0 else kv_num_heads // world_size),
            local_window_size=window_size,
            do_rotary=int(q_rotary is not None and k_rotary is not None),
            rotary_interleaved=interleaved,
        )
        model.model.graph.node.remove(node)
        model.model.graph.node.extend([gqa_node])

        if q_rotary is not None:
            model.model.graph.node.remove(q_rotary)
        if k_rotary is not None:
            model.model.graph.node.remove(k_rotary)

    return model

