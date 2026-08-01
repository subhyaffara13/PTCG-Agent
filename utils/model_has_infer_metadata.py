
def model_has_infer_metadata(model: ModelProto) -> bool:
    if model.metadata_props:
        for p in model.metadata_props:
            if p.key == "onnx.infer" and p.value == "onnxruntime.quant":
                return True
    return False

