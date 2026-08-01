
def run_ort_trt_xl(
    work_dir: str,
    version: str,
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
    use_cuda_graph=True,
    skip_warmup: bool = False,
):
    from demo_utils import initialize_pipeline  # noqa: PLC0415
    from engine_builder import EngineType  # noqa: PLC0415

    pipeline = initialize_pipeline(
        version=version,
        engine_type=EngineType.ORT_TRT,
        work_dir=work_dir,
        height=height,
        width=width,
        use_cuda_graph=use_cuda_graph,
        max_batch_size=max_batch_size,
        opt_batch_size=batch_size,
    )

    assert batch_size <= max_batch_size

    pipeline.load_resources(height, width, batch_size)

    def run_sd_xl_inference(prompt, negative_prompt, seed=None):
        return pipeline.run(
            prompt,
            negative_prompt,
            height,
            width,
            denoising_steps=steps,
            guidance=5.0,
            seed=seed,
        )

    def warmup():
        if skip_warmup:
            return
        prompt, negative = warmup_prompts()
        run_sd_xl_inference([prompt] * batch_size, [negative] * batch_size)

    # Run warm up, and measure GPU memory of two runs
    # The first run has algo search so it might need more memory
    first_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)
    second_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)

    warmup()

    model_name = pipeline.pipeline_info.name()
    image_filename_prefix = get_image_filename_prefix("ort_trt", model_name, batch_size, steps, disable_safety_checker)

    latency_list = []
    prompts, negative_prompt = example_prompts()
    for i, prompt in enumerate(prompts):
        if i >= num_prompts:
            break
        inference_start = time.time()
        # Use warmup mode here since non-warmup mode will save image to disk.
        images, pipeline_time = run_sd_xl_inference([prompt] * batch_size, [negative_prompt] * batch_size, seed=123)
        inference_end = time.time()
        latency = inference_end - inference_start
        latency_list.append(latency)
        print(f"End2End took {latency:.3f} seconds. Inference latency: {pipeline_time}")
        for k, image in enumerate(images):
            filename = f"{image_filename_prefix}_{i}_{k}.png"
            image.save(filename)
            print("Image saved to", filename)

    pipeline.teardown()

    from tensorrt import __version__ as trt_version  # noqa: PLC0415

    from onnxruntime import __version__ as ort_version  # noqa: PLC0415

    return {
        "model_name": model_name,
        "engine": "onnxruntime",
        "version": ort_version,
        "provider": f"tensorrt{trt_version})",
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

