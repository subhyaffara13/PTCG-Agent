
def autotune_at_compile_time_default() -> bool | None:
    return get_tristate_env("TORCHINDUCTOR_AUTOTUNE_AT_COMPILE_TIME")

