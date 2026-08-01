
def get_active_debug_mode() -> DebugMode | None:
    # Fast path: if no DebugMode is active, skip the stack walk
    if _ACTIVE_DEBUG_MODE_COUNT == 0:
        return None
    debug_mode = None
    for mode in _get_current_dispatch_mode_stack():
        if isinstance(mode, DebugMode):
            debug_mode = mode
            break
    return debug_mode

