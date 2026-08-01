
def _use_conv_autotune_backend(backend: str) -> bool:
    return backend.upper() in [
        x.strip() for x in config.max_autotune_conv_backends.upper().split(",")
    ]

