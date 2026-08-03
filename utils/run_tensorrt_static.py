import time

def run_tensorrt_static(
    work_dir: str,
    version: str,
    model_name: str,
    batch_size: int,
    disable_safety_checker: bool,
    height: int,
    width: int,
    steps: int,
    num_prompts: int,
    batch_count: int,
    start_memory,
    memory_monitor_type,
    max_batch_size: int,
    nvtx_profile: bool = False,
    use_cuda_graph: bool = True,
    skip_warmup: bool = False,
):
    print("[I] Initializing TensorRT accelerated StableDiffusionXL txt2img pipeline (static input shape)")

    from cuda import cudart  # noqa: PLC0415

    # Register TensorRT plugins
    from trt_utilities import init_trt_plugins  # noqa: PLC0415

    init_trt_plugins()

    assert batch_size <= max_batch_size

    from diffusion_models import PipelineInfo  # noqa: PLC0415

    pipeline_info = PipelineInfo(version)

    from engine_builder import EngineType, get_engine_paths  # noqa: PLC0415
    from pipeline_stable_diffusion import StableDiffusionPipeline  # noqa: PLC0415

    engine_type = EngineType.TRT
    onnx_dir, engine_dir, output_dir, framework_model_dir, timing_cache = get_engine_paths(
        work_dir, pipeline_info, engine_type
    )

    # Initialize pipeline
    pipeline = StableDiffusionPipeline(
        pipeline_info,
        scheduler="DDIM",
        output_dir=output_dir,
        verbose=False,
        nvtx_profile=nvtx_profile,
        max_batch_size=max_batch_size,
        use_cuda_graph=True,
        engine_type=engine_type,
    )

    # Load TensorRT engines and pytorch modules
    pipeline.backend.load_engines(
        engine_dir=engine_dir,
        framework_model_dir=framework_model_dir,
        onnx_dir=onnx_dir,
        onnx_opset=17,
        opt_batch_size=batch_size,
        opt_image_height=height,
        opt_image_width=width,
        static_batch=True,
        static_shape=True,
        enable_all_tactics=False,
        timing_cache=timing_cache,
    )

    # activate engines
    max_device_memory = max(pipeline.backend.max_device_memory(), pipeline.backend.max_device_memory())
    _, shared_device_memory = cudart.cudaMalloc(max_device_memory)
    pipeline.backend.activate_engines(shared_device_memory)

    # Here we use static batch and image size, so the resource allocation only need done once.
    # For dynamic batch and image size, some cost (like memory allocation) shall be included in latency.
    pipeline.load_resources(height, width, batch_size)

    def warmup():
        if skip_warmup:
            return
        prompt, negative = warmup_prompts()
        pipeline.run([prompt] * batch_size, [negative] * batch_size, height, width, denoising_steps=steps)

    # Run warm up, and measure GPU memory of two runs
    # The first run has algo search so it might need more memory
    first_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)
    second_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)

    warmup()

    image_filename_prefix = get_image_filename_prefix("trt", model_name, batch_size, steps, disable_safety_checker)

    latency_list = []
    prompts, negative_prompt = example_prompts()
    for i, prompt in enumerate(prompts):
        if i >= num_prompts:
            break
        inference_start = time.time()
        # Use warmup mode here since non-warmup mode will save image to disk.
        images, pipeline_time = pipeline.run(
            [prompt] * batch_size,
            [negative_prompt] * batch_size,
            height,
            width,
            denoising_steps=steps,
            seed=123,
        )
        inference_end = time.time()
        latency = inference_end - inference_start
        latency_list.append(latency)
        print(f"End2End took {latency:.3f} seconds. Inference latency: {pipeline_time}")
        for k, image in enumerate(images):
            image.save(f"{image_filename_prefix}_{i}_{k}.jpg")

    pipeline.teardown()

    import tensorrt as trt  # noqa: PLC0415

    return {
        "engine": "tensorrt",
        "version": trt.__version__,
        "provider": "default",
        "height": height,
        "width": width,
        "steps": steps,
        "batch_size": batch_size,
        "batch_count": batch_count,
        "num_prompts": num_prompts,
        "average_latency": sum(latency_list) / len(latency_list),
        "median_latency": statistics.median(latency_list),
        "first_run_memory_MB": first_run_memory,
        "second_run_memory_MB": second_run_memory,
        "enable_cuda_graph": use_cuda_graph,
    }

