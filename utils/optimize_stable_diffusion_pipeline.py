
def optimize_stable_diffusion_pipeline(
    input_dir: str,
    output_dir: str,
    overwrite: bool,
    use_external_data_format: bool | None,
    float16: bool,
    enable_runtime_optimization: bool,
    args,
):
    if os.path.exists(output_dir):
        if overwrite:
            shutil.rmtree(output_dir, ignore_errors=True)

    source_dir = Path(input_dir)
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    pipeline_type = _classify_pipeline_type(source_dir)
    model_list = _get_model_list(pipeline_type)

    _copy_extra_directory(source_dir, target_dir, model_list)

    return _optimize_sd_pipeline(
        source_dir,
        target_dir,
        pipeline_type,
        model_list,
        use_external_data_format,
        float16,
        args.bfloat16,
        args.force_fp32_ops,
        enable_runtime_optimization,
        args,
    )

