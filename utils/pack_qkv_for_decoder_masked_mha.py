
def pack_qkv_for_decoder_masked_mha(model_proto: ModelProto):
    onnx_model = OnnxModel(model_proto)
    output_name_to_node = onnx_model.output_name_to_node()

    nodes_to_add = []
    nodes_to_remove = []
    for node in onnx_model.nodes():
        if node.op_type == "DecoderMaskedMultiHeadAttention":
            if "past_key_cross" in node.input[1] and "past_value_cross" in node.input[2]:
                continue
            q_matmul = output_name_to_node[node.input[0]]
            k_matmul = output_name_to_node[node.input[1]]
            v_matmul = output_name_to_node[node.input[2]]

            q_weight = onnx_model.get_initializer(q_matmul.input[1])
            k_weight = onnx_model.get_initializer(k_matmul.input[1])
            v_weight = onnx_model.get_initializer(v_matmul.input[1])
            if not (q_weight and k_weight and v_weight):
                return False

            qw = NumpyHelper.to_array(q_weight)
            kw = NumpyHelper.to_array(k_weight)
            vw = NumpyHelper.to_array(v_weight)

            qkv_weight = np.concatenate([qw, kw, vw], axis=1)

            matmul_node_name = onnx_model.create_node_name("MatMul", name_prefix="MatMul_QKV")
            weight = onnx.helper.make_tensor(
                name=matmul_node_name + "_weight",
                data_type=(TensorProto.FLOAT if q_weight.data_type == 1 else TensorProto.FLOAT16),
                dims=[qkv_weight.shape[0], qkv_weight.shape[1]],
                vals=qkv_weight.flatten().tolist(),
            )

            model_proto.graph.initializer.extend([weight])

            matmul_node = onnx.helper.make_node(
                "MatMul",
                inputs=[q_matmul.input[0], matmul_node_name + "_weight"],
                outputs=[matmul_node_name + "_out"],
                name=matmul_node_name,
            )

            node.input[0] = matmul_node.output[0]
            node.input[1] = ""
            node.input[2] = ""

            nodes_to_add.extend([matmul_node])
            nodes_to_remove.extend([q_matmul, k_matmul, v_matmul])

    onnx_model.add_nodes(nodes_to_add)
    onnx_model.remove_nodes(nodes_to_remove)
    onnx_model.update_graph()

    onnx_model.topological_sort()

    return True

