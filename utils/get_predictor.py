
def get_predictor(
    sam2_dir: str,
    device: str | torch.device,
    dtype: torch.dtype,
    model_type="sam2_hiera_large",
    engine="torch",
    image_encoder_onnx_path: str = "",
    image_decoder_onnx_path: str = "",
    image_decoder_multi_onnx_path: str = "",
    provider: str = "CUDAExecutionProvider",
):
    sam2_model = load_sam2_model(sam2_dir, model_type, device=device)
    if engine == "torch":
        predictor = SAM2ImagePredictor(sam2_model)
    else:
        predictor = SAM2ImageOnnxPredictor(
            sam2_model,
            image_encoder_onnx_path=image_encoder_onnx_path,
            image_decoder_onnx_path=image_decoder_onnx_path,
            image_decoder_multi_onnx_path=image_decoder_multi_onnx_path,
            provider=provider,
            device=device,
            onnx_dtype=dtype,
        )
    return predictor

