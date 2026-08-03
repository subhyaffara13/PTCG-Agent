from typing import Any

def fx_forward_from_src_skip_result(
    src: str, globals: dict[str, Any], co_fields: dict[str, str] | None = None
) -> FunctionType:
    # we monkey patch FX to prevent infinite loop of trying to convert
    # our generated code
    result = original_forward_from_src(src, globals, co_fields)
    skip_code(result.__code__)
    return result

