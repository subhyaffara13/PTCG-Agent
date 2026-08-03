from typing import Any

def get_dynamo_config_override_for_compile_id(
    compile_id: CompileId | None,
    config_str: str,
) -> dict[str, Any] | None:
    """
    Get the dynamo config override for a given CompileId.

    Returns a dict of config patches to apply, or None if no override applies.
    """
    return _get_override_for_compile_id(
        compile_id,
        config_str,
        _create_dynamo_config_router,  # type: ignore[arg-type]
        "dynamo config",
    )

