
def run_ort(
    model_name: str,
    directory: str,
    provider: str,
    batch_size: int,
    disable_safety_checker: bool,
    height: int,
    width: int,
    steps: int,
    num_prompts: int,
    batch_count: int,
    start_memory,
    memory_monitor_type,
    tuning: bool,
    skip_warmup: bool = False,
):
    provider_and_options = provider
    if tuning and provider in ["CUDAExecutionProvider"]:
        provider_and_options = (provider, {"tunable_op_enable": 1, "tunable_op_tuning_enable": 1})

    load_start = time.time()
    pipe = get_ort_pipeline(model_name, directory, provider_and_options, disable_safety_checker)
    load_end = time.time()
    print(f"Model loading took {load_end - load_start} seconds")

    image_filename_prefix = get_image_filename_prefix("ort", model_name, batch_size, steps, disable_safety_checker)
    result = run_ort_pipeline(
        pipe,
        batch_size,
        image_filename_prefix,
        height,
        width,
        steps,
        num_prompts,
        batch_count,
        start_memory,
        memory_monitor_type,
        skip_warmup=skip_warmup,
    )

    result.update(
        {
            "model_name": model_name,
            "directory": directory,
            "provider": provider.replace("ExecutionProvider", ""),
            "disable_safety_checker": disable_safety_checker,
            "enable_cuda_graph": False,
        }
    )
    return result

