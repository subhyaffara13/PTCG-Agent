
def parse_qnn_json_file(qnn_json_file_path, qnn_input_output_tensor_dic):
    with open(qnn_json_file_path) as qnn_json_file:
        qnn_json = json.load(qnn_json_file)
        assert "graph" in qnn_json, "QNN converted json file not valid. Can't find graph."
        assert "tensors" in qnn_json["graph"], "QNN converted json file not valid. Can't find tensors."
        for qnn_tensor_name, qnn_tensor_attribute in qnn_json["graph"]["tensors"].items():
            # type:0 - QNN input tensor, type:1 - QNN output tensor
            assert (
                "type" in qnn_tensor_attribute
                and "data_type" in qnn_tensor_attribute
                and "dims" in qnn_tensor_attribute
            ), "QNN converted json file not valid. Can't find some keys from tensors"
            if qnn_tensor_attribute["type"] == 0 or qnn_tensor_attribute["type"] == 1:
                qnn_tensor = QnnTensorStruct()
                qnn_tensor.name = qnn_tensor_name
                qnn_tensor.onnx_data_type = qnn_data_type_to_onnx_data_type(qnn_tensor_attribute["data_type"])
                qnn_tensor.dim = qnn_tensor_attribute["dims"]
                qnn_input_output_tensor_dic[qnn_tensor_name] = qnn_tensor

    assert len(qnn_input_output_tensor_dic) > 1, (
        "Converted QNN model not valid. It should have at least 1 input & 1 output."
    )

