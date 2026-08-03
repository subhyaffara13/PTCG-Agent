import os

def _nvgemm_max_profiling_configs_default() -> int | None:
    env_val = os.environ.get("TORCHINDUCTOR_NVGEMM_MAX_PROFILING_CONFIGS", "5")
    if env_val.lower() in ("none", "all"):
        return None
    return int(env_val)

