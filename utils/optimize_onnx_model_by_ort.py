
def optimize_onnx_model_by_ort(onnx_model_path, ort_model_path, use_gpu, overwrite, model_fusion_statistics):
    if overwrite or not os.path.exists(ort_model_path):
        Path(ort_model_path).parent.mkdir(parents=True, exist_ok=True)
        from optimizer import get_fusion_statistics, optimize_by_onnxruntime  # noqa: PLC0415

        # Use onnxruntime to optimize model, which will be saved to *_ort.onnx
        _ = optimize_by_onnxruntime(
            onnx_model_path,
            use_gpu=use_gpu,
            optimized_model_path=ort_model_path,
            opt_level=99,
        )
        model_fusion_statistics[ort_model_path] = get_fusion_statistics(ort_model_path)
    else:
        logger.info(f"Skip optimization since model existed: {ort_model_path}")

