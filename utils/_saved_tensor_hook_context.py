from typing import Any

def _saved_tensor_hook_context(state: dict[str, Any]) -> Generator[None, None, None]:
    previous_state = getattr(_thread_local, "state", None)
    try:
        _thread_local.state = state
        yield
    finally:
        # Clean up: restore previous state or remove attribute
        if previous_state is not None:
            _thread_local.state = previous_state
        else:
            if hasattr(_thread_local, "state"):
                delattr(_thread_local, "state")

