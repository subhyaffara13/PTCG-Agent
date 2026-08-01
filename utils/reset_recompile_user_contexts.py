
def reset_recompile_user_contexts() -> None:
    """Clear any registered recompile user-context hooks (test helper)."""
    global _recompile_user_contexts
    _recompile_user_contexts = None

