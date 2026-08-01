
def has_external_data(model: ModelProto):
    """
    Check if the model has external data.

    Args:
        model (ModelProto): the model proto to check for external data.
    Returns:
        bool: True if the model has external data, False otherwise.
    """
    onnx_model = OnnxModel(model)
    for graph in onnx_model.graphs():
        for initializer in graph.initializer:
            if initializer.HasField("data_location") and initializer.data_location == TensorProto.EXTERNAL:
                return True
    return False


def has_external_data(onnx_model_path):
    original_model = onnx.load_model(str(onnx_model_path), load_external_data=False)
    for initializer in original_model.graph.initializer:
        if initializer.HasField("data_location") and initializer.data_location == onnx.TensorProto.EXTERNAL:
            return True
    return False

