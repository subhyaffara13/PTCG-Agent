
def get_engine_paths(
    work_dir: str, pipeline_info: PipelineInfo, engine_type: EngineType, framework_model_dir: str | None = None
):
    root_dir = work_dir or "."
    short_name = pipeline_info.short_name()

    # When both ORT_CUDA and ORT_TRT/TRT is used, we shall make sub directory for each engine since
    # ORT_CUDA need fp32 torch model, while ORT_TRT/TRT use fp16 torch model.
    onnx_dir = os.path.join(root_dir, engine_type.name, short_name, "onnx")
    engine_dir = os.path.join(root_dir, engine_type.name, short_name, "engine")
    output_dir = os.path.join(root_dir, engine_type.name, short_name, "output")

    timing_cache = os.path.join(root_dir, engine_type.name, "timing_cache")

    # Shared among ORT_CUDA, ORT_TRT and TRT engines, and need use load_model(..., always_download_fp16=True)
    # So that the shared model is always fp16.
    if framework_model_dir is None:
        framework_model_dir = os.path.join(root_dir, "torch_model")

    return onnx_dir, engine_dir, output_dir, framework_model_dir, timing_cache

