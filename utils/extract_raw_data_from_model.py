
def extract_raw_data_from_model(model: ModelProto):
    """
    Extract external data from model and return the external data as a list of tuples (name, value).
    Note this function does not handle external data that is not loaded into the model as raw data.

    Args:
        model (ModelProto): the model proto to extract external data from.
    Returns:
        (external_names, external_values): a tuple of two lists of external data names and values.
    """
    external_data = []
    onnx_model = OnnxModel(model)
    for graph in onnx_model.graphs():
        for initializer in graph.initializer:
            name = initializer.name

            if initializer.HasField("raw_data"):
                numpy_tensor = NumpyHelper.to_array(initializer)
                ort_value = OrtValue.ortvalue_from_numpy(numpy_tensor)
                external_data.append((name, ort_value))
                # mimic set_external_data
                set_external_data(initializer, location="foo.bin")
                initializer.name = name
                initializer.ClearField("raw_data")

    return zip(*external_data, strict=False)

