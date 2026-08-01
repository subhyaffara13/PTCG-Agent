
def prepare_environment(cache_dir, output_dir, use_gpu, provider=None):
    if cache_dir and not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if use_gpu:
        if provider == "dml":
            assert "DmlExecutionProvider" in onnxruntime.get_available_providers(), (
                "Please install onnxruntime-directml package to test GPU inference."
            )

        else:
            assert not set(onnxruntime.get_available_providers()).isdisjoint(
                ["CUDAExecutionProvider", "MIGraphXExecutionProvider"]
            ), "Please install onnxruntime-gpu package, or install migraphx, to test GPU inference."

    logger.info(f"PyTorch Version:{torch.__version__}")
    logger.info(f"Transformers Version:{transformers.__version__}")
    logger.info(f"OnnxRuntime Version:{onnxruntime.__version__}")

    # Support three major versions of PyTorch and OnnxRuntime, and up to 9 months of transformers.
    assert version.parse(torch.__version__) >= version.parse("1.10.0")
    assert version.parse(transformers.__version__) >= version.parse("4.12.0")
    assert version.parse(onnxruntime.__version__) >= version.parse("1.10.0")

