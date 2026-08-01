
def generate_wrapper_onnx_file(
    grap_name,
    model_file_name,
    qnn_input_tensor_dic,
    qnn_output_tensor_dic,
    disable_embed_mode,
    qnn_ctx_file,
    quantized_IO,
    qnn_sdk_version="unknown",
):
    graph_nodes = []
    ini_list = []
    value_infos = []

    model_inputs = []
    for qnn_input in sorted(qnn_input_tensor_dic.values(), key=lambda inp: inp.id):
        if qnn_input.is_quantized and not quantized_IO:
            q_scale_input_name = qnn_input.name + "_scale"
            q_offset_input_name = qnn_input.name + "_zp"
            q_scale = helper.make_tensor(q_scale_input_name, TensorProto.FLOAT, [], [qnn_input.scale])
            ini_list.append(q_scale)
            q_offset = helper.make_tensor(q_offset_input_name, qnn_input.onnx_data_type, [], [qnn_input.offset])
            ini_list.append(q_offset)
            input_name = qnn_input.name + "_dq"

            q_node = helper.make_node(
                "QuantizeLinear",
                name=qnn_input.name,
                inputs=[input_name, q_scale_input_name, q_offset_input_name],
                outputs=[qnn_input.name],
            )

            graph_nodes.append(q_node)
            model_inputs.append(helper.make_tensor_value_info(input_name, TensorProto.FLOAT, qnn_input.dim))
            value_infos.append(helper.make_tensor_value_info(qnn_input.name, qnn_input.onnx_data_type, qnn_input.dim))
        else:
            model_inputs.append(helper.make_tensor_value_info(qnn_input.name, qnn_input.onnx_data_type, qnn_input.dim))

    if disable_embed_mode:
        ep_cache_context_content = qnn_ctx_file
        ctx_embed_mode = 0
    else:
        with open(qnn_ctx_file, "rb") as file:
            ep_cache_context_content = file.read()
        ctx_embed_mode = 1

    qnn_ep_context_node = helper.make_node(
        "EPContext",
        name=grap_name,
        inputs=qnn_input_tensor_dic.keys(),
        outputs=qnn_output_tensor_dic.keys(),
        ep_cache_context=ep_cache_context_content,
        embed_mode=ctx_embed_mode,
        ep_sdk_version=qnn_sdk_version,
        source="Qnn",
        domain="com.microsoft",
    )
    graph_nodes.append(qnn_ep_context_node)

    model_outputs = []
    for qnn_output in sorted(qnn_output_tensor_dic.values(), key=lambda out: out.id):
        if qnn_output.is_quantized and not quantized_IO:
            dq_scale_input_name = qnn_output.name + "_scale"
            dq_offset_input_name = qnn_output.name + "_zp"
            dq_scale = helper.make_tensor(dq_scale_input_name, TensorProto.FLOAT, [], [qnn_output.scale])
            ini_list.append(dq_scale)
            dq_offset = helper.make_tensor(dq_offset_input_name, qnn_output.onnx_data_type, [], [qnn_output.offset])
            ini_list.append(dq_offset)
            output_name = qnn_output.name + "_dq"

            dq_node = helper.make_node(
                "DequantizeLinear",
                name=output_name,
                inputs=[qnn_output.name, dq_scale_input_name, dq_offset_input_name],
                outputs=[output_name],
            )

            graph_nodes.append(dq_node)
            model_outputs.append(helper.make_tensor_value_info(output_name, TensorProto.FLOAT, qnn_output.dim))
            value_infos.append(
                helper.make_tensor_value_info(qnn_output.name, qnn_output.onnx_data_type, qnn_output.dim)
            )
        else:
            model_outputs.append(
                helper.make_tensor_value_info(qnn_output.name, qnn_output.onnx_data_type, qnn_output.dim)
            )

    graph_def = helper.make_graph(graph_nodes, "qnn-onnx-model", model_inputs, model_outputs, ini_list, "", value_infos)

    model_def = helper.make_model(graph_def, producer_name="MS")

    onnx.save(model_def, model_file_name)

