import os

def get_onnx_file_path(
    onnx_dir: str,
    model_name: str,
    input_count: int,
    optimized_by_script: bool,
    use_gpu: bool,
    precision: Precision,
    optimized_by_onnxruntime: bool,
    use_external_data: bool,
):
    from re import sub  # noqa: PLC0415

    normalized_model_name = sub(r"[^a-zA-Z0-9_]", "_", model_name)

    if not optimized_by_script:
        filename = f"{normalized_model_name}_{input_count}"
    else:
        device = "gpu" if use_gpu else "cpu"
        filename = f"{normalized_model_name}_{input_count}_{precision}_{device}"

    if optimized_by_onnxruntime:
        filename += "_ort"

    directory = onnx_dir
    # ONNXRuntime will not write external data so the raw and optimized models shall be in same directory.
    if use_external_data and not optimized_by_onnxruntime:
        directory = os.path.join(onnx_dir, filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

    return os.path.join(directory, f"{filename}.onnx")

