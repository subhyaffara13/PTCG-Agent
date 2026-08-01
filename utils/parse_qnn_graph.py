
def parse_qnn_graph(qnn_graph, qnn_input_tensor_dic, qnn_output_tensor_dic):
    is_qnn_converter_json = False
    graph_name = qnn_graph["info"]["graphName"]
    raw_inputs = qnn_graph["info"]["graphInputs"]
    raw_outputs = qnn_graph["info"]["graphOutputs"]

    for raw_input in raw_inputs:
        tensor_info = raw_input["info"]
        qnn_tensor = QnnTensorStruct()
        qnn_tensor.name = tensor_info["name"]
        qnn_tensor.onnx_data_type = qnn_data_type_to_onnx_data_type(tensor_info["dataType"], is_qnn_converter_json)
        qnn_tensor.is_quantized = is_quantized_data_type(tensor_info["dataType"], is_qnn_converter_json)
        qnn_tensor.dim = tensor_info["dimensions"]
        if (
            tensor_info["quantizeParams"]["definition"] == "QNN_DEFINITION_DEFINED"
            and tensor_info["quantizeParams"]["quantizationEncoding"] == "QNN_QUANTIZATION_ENCODING_SCALE_OFFSET"
        ):
            qnn_tensor.scale = tensor_info["quantizeParams"]["scaleOffset"]["scale"]
            qnn_tensor.offset = 0 - tensor_info["quantizeParams"]["scaleOffset"]["offset"]
        qnn_input_tensor_dic[qnn_tensor.name] = qnn_tensor

    for raw_output in raw_outputs:
        tensor_info = raw_output["info"]
        qnn_tensor = QnnTensorStruct()
        qnn_tensor.name = tensor_info["name"]
        qnn_tensor.onnx_data_type = qnn_data_type_to_onnx_data_type(tensor_info["dataType"], is_qnn_converter_json)
        qnn_tensor.is_quantized = is_quantized_data_type(tensor_info["dataType"], is_qnn_converter_json)
        qnn_tensor.dim = tensor_info["dimensions"]
        if (
            tensor_info["quantizeParams"]["definition"] == "QNN_DEFINITION_DEFINED"
            and tensor_info["quantizeParams"]["quantizationEncoding"] == "QNN_QUANTIZATION_ENCODING_SCALE_OFFSET"
        ):
            qnn_tensor.scale = tensor_info["quantizeParams"]["scaleOffset"]["scale"]
            qnn_tensor.offset = 0 - tensor_info["quantizeParams"]["scaleOffset"]["offset"]
        qnn_output_tensor_dic[qnn_tensor.name] = qnn_tensor

    assert len(qnn_input_tensor_dic) >= 1 and len(qnn_output_tensor_dic) >= 1, (
        "Converted QNN model not valid. It should have at least 1 input & 1 output."
    )

    return graph_name

