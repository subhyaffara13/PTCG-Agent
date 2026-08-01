
def get_gpu_type() -> NVIDIA_GPU_TYPE:
    gpu_info = torch.utils.collect_env.get_gpu_info(torch.utils.collect_env.run) or ""
    if "V100" in gpu_info:
        return NVIDIA_GPU_TYPE.VOLTA
    elif "A100" in gpu_info:
        return NVIDIA_GPU_TYPE.AMPERE
    elif "H100" in gpu_info:
        return NVIDIA_GPU_TYPE.HOPPER
    elif any(gpu in gpu_info for gpu in ("B100", "B200", "B300")):
        return NVIDIA_GPU_TYPE.BLACKWELL
    else:
        # for other gpu types, assume Ampere
        return NVIDIA_GPU_TYPE.AMPERE


def get_gpu_type() -> str:
    avail_gpus = [x for x in GPU_TYPES if getattr(torch, x).is_available()]
    assert len(avail_gpus) <= 1
    gpu_type = "cuda" if len(avail_gpus) == 0 else avail_gpus.pop()
    return gpu_type

