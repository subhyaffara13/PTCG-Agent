
def force_fallback(op: torch._ops.OpOverload):
    """
    A context manager to force fallback an op. Used in unit test
    for FallbackKernel.
    """
    assert isinstance(op, torch._ops.OpOverload), (
        "Only OpOverload to make the clean up easier"
    )
    old_handler = lowerings.get(op)
    try:
        register_lowering(op)(fallback_handler(op))
        yield
    finally:
        if old_handler:
            lowerings[op] = old_handler
        else:
            lowerings.pop(op)

