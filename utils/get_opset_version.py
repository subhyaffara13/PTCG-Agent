
def get_opset_version(model: ModelProto) -> int:
    ai_onnx_domain = [opset for opset in model.opset_import if not opset.domain or opset.domain == "ai.onnx"]
    if len(ai_onnx_domain) != 1:
        raise ValueError("Failed to find proper ai.onnx domain")
    opset_version = ai_onnx_domain[0].version

    return opset_version

