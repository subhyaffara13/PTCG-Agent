
def get_hook_for_recompile_user_context() -> list[Callable[[], str]] | None:
    return _recompile_user_contexts

