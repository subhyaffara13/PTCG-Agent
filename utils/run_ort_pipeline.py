import time

def run_ort_pipeline(
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
    skip_warmup: bool = False,
):
    from diffusers import OnnxStableDiffusionPipeline  # noqa: PLC0415

    assert isinstance(pipe, OnnxStableDiffusionPipeline)

    prompts, negative_prompt = example_prompts()

    def warmup():
        if skip_warmup:
            return
        prompt, negative = warmup_prompts()
        pipe(
            prompt=[prompt] * batch_size,
            height=height,
            width=width,
            num_inference_steps=steps,
            negative_prompt=[negative] * batch_size,
        )

    # Run warm up, and measure GPU memory of two runs
    # cuDNN/MIOpen The first run has  algo search so it might need more memory)
    first_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)
    second_run_memory = measure_gpu_memory(memory_monitor_type, warmup, start_memory)

    warmup()

    latency_list = []
    for i, prompt in enumerate(prompts):
        if i >= num_prompts:
            break
        inference_start = time.time()
        images = pipe(
            prompt=[prompt] * batch_size,
            height=height,
            width=width,
            num_inference_steps=steps,
            negative_prompt=[negative_prompt] * batch_size,
        ).images
        inference_end = time.time()
        latency = inference_end - inference_start
        latency_list.append(latency)
        print(f"Inference took {latency:.3f} seconds")
        for k, image in enumerate(images):
            image.save(f"{image_filename_prefix}_{i}_{k}.jpg")

    from onnxruntime import __version__ as ort_version  # noqa: PLC0415

    return {
        "engine": "onnxruntime",
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

