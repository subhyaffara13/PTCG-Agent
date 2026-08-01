
def optimize_sam2_model(onnx_model_path, optimized_model_path, float16: bool, use_gpu: bool):
    print(f"Optimizing {onnx_model_path} to {optimized_model_path} with float16={float16} and use_gpu={use_gpu}...")

    # Import from source directory.
    transformers_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if transformers_dir not in sys.path:
        sys.path.insert(0, transformers_dir)
    from optimizer import optimize_model  # noqa: PLC0415

    optimized_model = optimize_model(onnx_model_path, model_type="sam2", opt_level=1, use_gpu=use_gpu)
    if float16:
        optimized_model.convert_float_to_float16(keep_io_types=False)
    optimized_model.save_model_to_file(optimized_model_path)

