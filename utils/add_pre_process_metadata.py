
def add_pre_process_metadata(model: ModelProto):
    """Tag the model that it went through quantization pre-processing"""
    metadata_props = {"onnx.quant.pre_process": "onnxruntime.quant"}
    if model.metadata_props:
        for prop in model.metadata_props:
            metadata_props.update({prop.key: prop.value})
    onnx.helper.set_model_props(model, metadata_props)

