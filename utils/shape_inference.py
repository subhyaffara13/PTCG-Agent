
def shape_inference(onnx_path: str, use_external_data_format: bool = True):
    """Shape inference on an onnx file, which will be overwritten.

    Args:
        onnx_path (str): Path of onnx model
        use_external_data_format(bool): output tensors to external data or not.
    """
    # Run symbolic shape inference to walk around ORT shape inference issue for subgraph.
    from onnxruntime.tools.symbolic_shape_infer import SymbolicShapeInference  # noqa: PLC0415

    model = onnx.load_model(onnx_path, load_external_data=True)
    out = SymbolicShapeInference.infer_shapes(model, auto_merge=True, guess_output_rank=False)
    if out:
        OnnxModel.save(out, onnx_path, save_as_external_data=use_external_data_format)
    else:
        logger.warning("Failed to run symbolic shape inference on the model.")

