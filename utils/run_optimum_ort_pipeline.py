import time

def run_optimum_ort_pipeline(
    pipe,
    batch_size: int,
    image_filename_prefix: str,
    height,
    width,
    steps,
    num_prompts,
    batch_count,
    start_memory,
    memory_monitor_type,
    use_num_images_per_prompt=False,
    skip_warmup=False,
):
    print("Pipeline type", type(pipe))
    from optimum.onnxruntime.modeling_diffusion import ORTFluxPipeline  # noqa: PLC0415

    is_flux = isinstance(pipe, ORTFluxPipeline)

    prompts, negative_prompt = example_prompts()

    def warmup():
        if skip_warmup:
            return
        prompt, negative = warmup_prompts()
        extra_kwargs = get_negative_prompt_kwargs(negative, use_num_images_per_prompt, is_flux, batch_size)
        if use_num_images_per_prompt:
            pipe(
                prompt=prompt,
                height=height,
                width=width,
                num_inference_steps=steps,
                num_images_per_prompt=batch_count,
                **extra_kwargs,
            )
        else:
            pipe(prompt=[prompt] * batch_size, height=height, width=width, num_inference_steps=steps, **extra_kwargs)

    # Run warm up, and measure GPU memory of two runs.
    # The first run has algo search for cuDNN/MIOpen, so it might need more memory.
    first_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)
    second_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)

    warmup()

    extra_kwargs = get_negative_prompt_kwargs(negative_prompt, use_num_images_per_prompt, is_flux, batch_size)

    latency_list = []
    for i, prompt in enumerate(prompts):
        if i >= num_prompts:
            break
        inference_start = time.time()
        if use_num_images_per_prompt:
            images = pipe(
                prompt=prompt,
                height=height,
                width=width,
                num_inference_steps=steps,
                num_images_per_prompt=batch_size,
                **extra_kwargs,
            ).images
        else:
            images = pipe(
                prompt=[prompt] * batch_size, height=height, width=width, num_inference_steps=steps, **extra_kwargs
            ).images
        inference_end = time.time()
        latency = inference_end - inference_start
        latency_list.append(latency)
        print(f"Inference took {latency:.3f} seconds")
        for k, image in enumerate(images):
            image.save(f"{image_filename_prefix}_{i}_{k}.jpg")

    from onnxruntime import __version__ as ort_version  # noqa: PLC0415

    return {
        "engine": "optimum_ort",
        "version": ort_version,
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
    }

