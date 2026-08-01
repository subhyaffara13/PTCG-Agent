
def model_has_pre_process_metadata(model: ModelProto) -> bool:
    """Check the model whether it went through quantization pre-processing"""
    if model.metadata_props:
        for prop in model.metadata_props:
            if prop.key == "onnx.quant.pre_process" and prop.value == "onnxruntime.quant":
                return True
    return False

