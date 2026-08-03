import os

def initialize_pipeline(
    version="xl-turbo",
    is_refiner: bool = False,
    is_inpaint: bool = False,
    engine_type=EngineType.ORT_CUDA,
    work_dir: str = ".",
    engine_dir=None,
    onnx_opset: int = 17,
    scheduler="EulerA",
    height=512,
    width=512,
    nvtx_profile=False,
    use_cuda_graph=True,
    build_dynamic_batch=False,
    build_dynamic_shape=False,
    min_image_size: int = 512,
    max_image_size: int = 1024,
    max_batch_size: int = 16,
    opt_batch_size: int = 1,
    build_all_tactics: bool = False,
    do_classifier_free_guidance: bool = False,
    lcm: bool = False,
    controlnet=None,
    lora_weights=None,
    lora_scale: float = 1.0,
    use_fp16_vae: bool = True,
    use_vae: bool = True,
    framework_model_dir: str | None = None,
    max_cuda_graphs: int = 1,
):
    pipeline_info = PipelineInfo(
        version,
        is_refiner=is_refiner,
        is_inpaint=is_inpaint,
        use_vae=use_vae,
        min_image_size=min_image_size,
        max_image_size=max_image_size,
        use_fp16_vae=use_fp16_vae,
        use_lcm=lcm,
        do_classifier_free_guidance=do_classifier_free_guidance,
        controlnet=controlnet,
        lora_weights=lora_weights,
        lora_scale=lora_scale,
    )

    input_engine_dir = engine_dir

    onnx_dir, engine_dir, output_dir, framework_model_dir, timing_cache = get_engine_paths(
        work_dir=work_dir, pipeline_info=pipeline_info, engine_type=engine_type, framework_model_dir=framework_model_dir
    )

    pipeline = StableDiffusionPipeline(
        pipeline_info,
        scheduler=scheduler,
        output_dir=output_dir,
        verbose=False,
        nvtx_profile=nvtx_profile,
        max_batch_size=max_batch_size,
        use_cuda_graph=use_cuda_graph,
        framework_model_dir=framework_model_dir,
        engine_type=engine_type,
    )

    import_engine_dir = None
    if input_engine_dir:
        if not os.path.exists(input_engine_dir):
            raise RuntimeError(f"--engine_dir directory does not exist: {input_engine_dir}")

        # Support importing from optimized diffusers onnx pipeline
        if engine_type == EngineType.ORT_CUDA and os.path.exists(os.path.join(input_engine_dir, "model_index.json")):
            import_engine_dir = input_engine_dir
        else:
            engine_dir = input_engine_dir

    opt_image_height = pipeline_info.default_image_size() if build_dynamic_shape else height
    opt_image_width = pipeline_info.default_image_size() if build_dynamic_shape else width

    if engine_type == EngineType.ORT_CUDA:
        pipeline.backend.build_engines(
            engine_dir=engine_dir,
            framework_model_dir=framework_model_dir,
            onnx_dir=onnx_dir,
            tmp_dir=os.path.join(work_dir or ".", engine_type.name, pipeline_info.short_name(), "tmp"),
            device_id=torch.cuda.current_device(),
            import_engine_dir=import_engine_dir,
            max_cuda_graphs=max_cuda_graphs,
        )
    elif engine_type == EngineType.ORT_TRT:
        pipeline.backend.build_engines(
            engine_dir,
            framework_model_dir,
            onnx_dir,
            onnx_opset,
            opt_image_height=opt_image_height,
            opt_image_width=opt_image_width,
            opt_batch_size=opt_batch_size,
            static_batch=not build_dynamic_batch,
            static_image_shape=not build_dynamic_shape,
            max_workspace_size=0,
            device_id=torch.cuda.current_device(),
            timing_cache=timing_cache,
        )
    elif engine_type == EngineType.TRT:
        pipeline.backend.load_engines(
            engine_dir,
            framework_model_dir,
            onnx_dir,
            onnx_opset,
            opt_batch_size=opt_batch_size,
            opt_image_height=opt_image_height,
            opt_image_width=opt_image_width,
            static_batch=not build_dynamic_batch,
            static_shape=not build_dynamic_shape,
            enable_all_tactics=build_all_tactics,
            timing_cache=timing_cache,
        )
    elif engine_type == EngineType.TORCH:
        pipeline.backend.build_engines(framework_model_dir)
    else:
        raise RuntimeError("invalid engine type")

    return pipeline

