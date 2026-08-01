
def model_has_external_data(model_path: Path):
    model = onnx.load(model_path.as_posix(), load_external_data=False)
    return any(external_data_helper.uses_external_data(intializer) for intializer in model.graph.initializer)

