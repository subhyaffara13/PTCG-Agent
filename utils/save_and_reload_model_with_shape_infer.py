
def save_and_reload_model_with_shape_infer(model: ModelProto) -> ModelProto:
    with tempfile.TemporaryDirectory(prefix="ort.quant.") as quant_tmp_dir:
        model_copy = copy.deepcopy(model)
        model_path = Path(quant_tmp_dir).joinpath("model.onnx")
        onnx.save_model(model_copy, model_path.as_posix(), save_as_external_data=True)
        return load_model_with_shape_infer(model_path)

