
def _get_saved_tensor_hook_context() -> dict[str, Any] | None:
    return getattr(_thread_local, "state", None)

