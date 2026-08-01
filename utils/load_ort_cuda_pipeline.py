
def load_ort_cuda_pipeline(name, engine, use_control_net=False, enable_cuda_graph=True, work_dir="."):
    version = PipelineInfo.supported_models()[name]
    guidance_scale = 0.0
    pipeline_info = PipelineInfo(
        version,
        use_vae=True,
        use_fp16_vae=True,
        do_classifier_free_guidance=(guidance_scale > 1.0),
        controlnet=["canny"] if use_control_net else [],
    )

    engine_type = EngineType.ORT_CUDA if engine == "ort_cuda" else EngineType.ORT_TRT
    onnx_dir, engine_dir, output_dir, framework_model_dir, _ = get_engine_paths(
        work_dir=work_dir, pipeline_info=pipeline_info, engine_type=engine_type
    )

    pipeline = StableDiffusionPipeline(
        pipeline_info,
        scheduler="EulerA",
        max_batch_size=32,
        use_cuda_graph=enable_cuda_graph,
        framework_model_dir=framework_model_dir,
        output_dir=output_dir,
        engine_type=engine_type,
    )

    pipeline.backend.build_engines(
        engine_dir=engine_dir,
        framework_model_dir=framework_model_dir,
        onnx_dir=onnx_dir,
        device_id=torch.cuda.current_device(),
    )

    return pipeline

