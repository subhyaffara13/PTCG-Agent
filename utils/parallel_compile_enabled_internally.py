
def parallel_compile_enabled_internally() -> bool:
    """
    TODO: Remove when parallel compiled is fully enabled internally. For rollout, use a
    knob to enable / disable. The justknob should not be performed at import, however.
    So for fbcode, we assign compile_threads to 'None' below and initialize lazily in
    async_compile.py.
    """
    ENABLE_PARALLEL_COMPILE_VERSION = 1

    jk_name = "pytorch/inductor:enable_parallel_compile_version"
    version = torch._utils_internal.justknobs_getval_int(jk_name)
    return ENABLE_PARALLEL_COMPILE_VERSION >= version

