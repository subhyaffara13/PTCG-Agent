
def enable_torchbind_tracing():
    """Context manager that acts as a feature flag to enable torchbind tracing
    behavior. Once torchbind tracing has been stabilized, we can remove this and
    turn it always on.
    """
    try:
        KNOWN_TYPES.append(torch.ScriptObject)
        torch.ScriptMethod.__call__ = torchbind_method_redispatch  # type: ignore[method-assign]
        yield
    finally:
        if KNOWN_TYPES.pop() is not torch.ScriptObject:
            raise AssertionError(
                "Someone else messed with KNOWN_TYPES during tracing, exploding."
            )
        torch.ScriptMethod.__call__ = _orig_scriptmethod_call  # type: ignore[method-assign]

