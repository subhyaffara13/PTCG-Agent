
def run_torch_pipeline(
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
    skip_warmup=False,
):
    prompts, negative_prompt = example_prompts()

    import diffusers  # noqa: PLC0415

    is_flux = isinstance(pipe, diffusers.FluxPipeline)

    def warmup():
        if skip_warmup:
            return
        prompt, negative = warmup_prompts()
        extra_kwargs = get_negative_prompt_kwargs(negative, False, is_flux, batch_size)
        pipe(prompt=[prompt] * batch_size, height=height, width=width, num_inference_steps=steps, **extra_kwargs)

    # Run warm up, and measure GPU memory of two runs (The first run has cuDNN algo search so it might need more memory)
    first_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)
    second_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)

    warmup()

    torch.set_grad_enabled(False)

    latency_list = []
    for i, prompt in enumerate(prompts):
        if i >= num_prompts:
            break
        torch.cuda.synchronize()
        inference_start = time.time()
        extra_kwargs = get_negative_prompt_kwargs(negative_prompt, False, is_flux, batch_size)
        images = pipe(
            prompt=[prompt] * batch_size,
            height=height,
            width=width,
            num_inference_steps=steps,
            **extra_kwargs,
        ).images

        torch.cuda.synchronize()
        inference_end = time.time()
        latency = inference_end - inference_start
        latency_list.append(latency)
        print(f"Inference took {latency:.3f} seconds")
        for k, image in enumerate(images):
            image.save(f"{image_filename_prefix}_{i}_{k}.jpg")

    return {
        "engine": "torch",
        "version": torch.__version__,
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

