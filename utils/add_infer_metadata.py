
def add_infer_metadata(model: ModelProto):
    metadata_props = {"onnx.infer": "onnxruntime.quant"}
    if model.metadata_props:
        for p in model.metadata_props:
            metadata_props.update({p.key: p.value})
    onnx.helper.set_model_props(model, metadata_props)

