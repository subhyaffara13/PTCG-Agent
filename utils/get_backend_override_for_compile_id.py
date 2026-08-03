from typing import Any

def get_backend_override_for_compile_id(
    compile_id: CompileId | None,
    config_str: str,
) -> Any:
    """
    Get the backend override for a given CompileId.

    Returns the backend function to use, or None if no override applies.
    """
    return _get_override_for_compile_id(
        compile_id,
        config_str,
        _create_backend_router,
        "torch.compile backend",
    )

