
def get_ort_environment_variables():
    # Environment variables might impact ORT performance on transformer models. Note that they are for testing only.
    env_names = [
        "ORT_DISABLE_FUSED_ATTENTION",
        "ORT_ENABLE_FUSED_CAUSAL_ATTENTION",
        "ORT_DISABLE_FUSED_CROSS_ATTENTION",
        "ORT_DISABLE_TRT_FLASH_ATTENTION",
        "ORT_DISABLE_MEMORY_EFFICIENT_ATTENTION",
        "ORT_TRANSFORMER_OPTIONS",
        "ORT_CUDA_GEMM_OPTIONS",
    ]
    env = ""
    for name in env_names:
        value = os.getenv(name)
        if value is None:
            continue
        if env:
            env += ","
        env += f"{name}={value}"
    return env

