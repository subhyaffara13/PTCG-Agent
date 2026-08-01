
def get_device_and_memory_breakdown() -> tuple[torch.device, int, int, int]:
    if torch.cuda.is_available():
        device = torch.device("cuda")
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        # Use mem_get_info to get actual free memory: device_properties().total_memory returns the physical device
        # total which ignores CUDA context and driver overhead (~0.5 GiB), leading to overcommit.
        free_memory, total_memory = torch.cuda.mem_get_info(device)
        reserved_memory = torch.cuda.memory_reserved(device)
        allocated_memory = total_memory - free_memory
    elif is_torch_xpu_available():
        device = torch.device("xpu")
        torch.xpu.empty_cache()
        torch.xpu.synchronize()
        total_memory = torch.xpu.get_device_properties(device).total_memory
        reserved_memory = torch.xpu.memory_reserved(device)
        allocated_memory = torch.xpu.memory_allocated(device)
    elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device = torch.device("mps")
        total_memory = torch.mps.recommended_max_memory()
        allocated_memory = torch.mps.current_allocated_memory()
        reserved_memory = torch.mps.driver_allocated_memory()
    else:
        device = torch.device("cpu")
        if is_psutil_available():
            total_memory = psutil.virtual_memory().total
            allocated_memory = psutil.Process().memory_info().rss
            reserved_memory = allocated_memory
        else:
            logger.error(
                "Cannot get memory breakdown on CPU without psutil: returning 0 for all memory values. Please install "
                "psutil to get an actual memory breakdown."
            )
            total_memory = 0
            reserved_memory = 0
            allocated_memory = 0

    return device, total_memory, reserved_memory, allocated_memory

