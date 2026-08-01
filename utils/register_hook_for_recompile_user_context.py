
def register_hook_for_recompile_user_context(hook: Callable[[], str]) -> None:
    """
    Register a hook to be called when a recompile is triggered. The hook
    should return a string describing user contexts that are not available
    to the compiler, such as the current training epoch. This is useful for
    debugging and data analysis for recompile. For data retention purposes,
    the user context string is capped at 256 characters.
    """
    global _recompile_user_contexts
    if _recompile_user_contexts is None:
        _recompile_user_contexts = []
    _recompile_user_contexts.append(hook)

