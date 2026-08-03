import time
from pathlib import Path


def run_optimum_ort(
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
    use_io_binding: bool = False,
    skip_warmup: bool = False,
):
    load_start = time.time()
    pipe = get_optimum_ort_pipeline(
        model_name, directory, provider, disable_safety_checker, use_io_binding=use_io_binding
    )
    load_end = time.time()
    print(f"Model loading took {load_end - load_start} seconds")

    full_model_name = model_name + "_" + Path(directory).name if directory else model_name
    image_filename_prefix = get_image_filename_prefix(
        "optimum", full_model_name, batch_size, steps, disable_safety_checker
    )
    result = run_optimum_ort_pipeline(
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

