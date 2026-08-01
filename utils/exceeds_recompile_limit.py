
def exceeds_recompile_limit(
    cache_size: CacheSizeRelevantForFrame, compile_id: CompileId
) -> tuple[bool, str]:
    """
    Checks if we are exceeding the cache size limit.
    """
    if cache_size.will_compilation_exceed_accumulated_limit():
        return True, "accumulated_recompile_limit"
    if cache_size.will_compilation_exceed_specific_limit(config.recompile_limit):
        return True, "recompile_limit"
    # NOTE this check is needed in the case that the frame's cache doesn't grow
    # and we keep recompiling. This can happen if the guard guard_manager becomes invalidated,
    # e.g. due to guarded objects being freed. This technically makes the
    # will_compilation_exceed_accumulated_limit check unnecessary, but we will keep the
    # check in case we have a better fix in the future.
    assert compile_id.frame_compile_id is not None
    if compile_id.frame_compile_id >= config.accumulated_recompile_limit:
        return True, "accumulated_recompile_limit"
    return False, ""

