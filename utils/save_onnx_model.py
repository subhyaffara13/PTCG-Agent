
def save_onnx_model(onnx_model: onnx.ModelProto, output_path: str, data_path: str):
    onnx.save(
        onnx_model,
        output_path,
        save_as_external_data=True,
        all_tensors_to_one_file=True,
        location=data_path,
        size_threshold=1024,
        convert_attribute=False,
    )

