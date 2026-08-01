
def _nvml_based_avail() -> bool:
    return os.getenv("PYTORCH_NVML_BASED_CUDA_CHECK") == "1"

