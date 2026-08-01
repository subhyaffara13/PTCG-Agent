
def requires_gpu_with_enough_memory(min_mem_required):
    def inner(fn):
        total_memory = sys.maxsize
        if torch.xpu.is_available():
            total_memory = torch.xpu.get_device_properties().total_memory
        elif torch.cuda.is_available():
            total_memory = torch.cuda.get_device_properties().total_memory
        if (
            not (torch.cuda.is_available() or torch.xpu.is_available())
            or total_memory < min_mem_required
        ):
            return unittest.skip(
                f"Only if the GPU device has at least {min_mem_required / 1e9:.3f}GB memory to be safe"
            )(fn)
        else:
            return fn

    return inner

