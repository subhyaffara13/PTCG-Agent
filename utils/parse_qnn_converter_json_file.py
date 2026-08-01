
def parse_qnn_converter_json_file(qnn_convert_json, qnn_input_tensor_dic, qnn_output_tensor_dic):
    is_qnn_converter_json = True
    for qnn_tensor_name, qnn_tensor_attribute in qnn_convert_json["graph"]["tensors"].items():
        # type:0 - QNN input tensor, type:1 - QNN output tensor
        assert (
            "type" in qnn_tensor_attribute
            and "data_type" in qnn_tensor_attribute
            and "dims" in qnn_tensor_attribute
            and "id" in qnn_tensor_attribute
            and "quant_params" in qnn_tensor_attribute
        ), "QNN converted json file not valid. Can't find some keys from tensors"

        # If tensor is not IO, ignore it
        if qnn_tensor_attribute["type"] not in [0, 1]:
            continue

        # Get all graph inputs & output
        qnn_tensor = QnnTensorStruct(
            name=qnn_tensor_name,
            onnx_data_type=qnn_data_type_to_onnx_data_type(qnn_tensor_attribute["data_type"], is_qnn_converter_json),
            is_quantized=is_quantized_data_type(qnn_tensor_attribute["data_type"], is_qnn_converter_json),
            dim=qnn_tensor_attribute["dims"],
            id=qnn_tensor_attribute["id"],
        )

        if (
            qnn_tensor_attribute["quant_params"]["definition"] == 1
            and qnn_tensor_attribute["quant_params"]["encoding"] == 0
        ):
            qnn_tensor.scale = qnn_tensor_attribute["quant_params"]["scale_offset"]["scale"]
            qnn_tensor.offset = -qnn_tensor_attribute["quant_params"]["scale_offset"]["offset"]

        if qnn_tensor_attribute["type"] == 0:
            qnn_input_tensor_dic[qnn_tensor_name] = qnn_tensor
        else:
            qnn_output_tensor_dic[qnn_tensor_name] = qnn_tensor

    assert len(qnn_input_tensor_dic) >= 1 and len(qnn_output_tensor_dic) >= 1, (
        "Converted QNN model not valid. It should have at least 1 input & 1 output."
    )

