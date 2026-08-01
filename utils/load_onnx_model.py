
def load_onnx_model(
    model_id: str, onnx_path: str | None = None, provider="CUDAExecutionProvider", use_io_binding: bool = False
):
    """Load onnx model given pretrained model name and optional ONNX model path. If onnx_path is None,
    the default onnx model from optimum will be used.

    Args:
        model_id (str): pretrained model name or checkpoint path
        onnx_path (Optional[str], optional): path of onnx model to evaluate. Defaults to None.

    Returns:
        model: ORTModel for the onnx model
        onnx_path: the path of onnx model
    """

    if onnx_path is None:
        # Export onnx to a sub-directory named by the model id
        model = ORTModelForQuestionAnswering.from_pretrained(
            model_id, export=True, provider=provider, use_io_binding=use_io_binding
        )
        save_onnx_dir = os.path.join(".", model_id)
        model.save_pretrained(save_onnx_dir)
        onnx_path = os.path.join(save_onnx_dir, "model.onnx")
        print("Model is exported to onnx file:", onnx_path)
    else:
        model = ORTModelForQuestionAnswering.from_pretrained(
            os.path.dirname(onnx_path),
            file_name=Path(onnx_path).name,
            provider=provider,
            use_io_binding=use_io_binding,
            # provider_options={"enable_skip_layer_norm_strict_mode": True},
        )

    return model, onnx_path

