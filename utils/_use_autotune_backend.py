
def _use_autotune_backend(backend: str) -> bool:
    return backend.upper() in [
        x.strip() for x in config.max_autotune_gemm_backends.upper().split(",")
    ]

