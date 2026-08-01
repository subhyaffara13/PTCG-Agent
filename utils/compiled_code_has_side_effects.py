
def compiled_code_has_side_effects(code: types.CodeType) -> bool:
    """Return whether Dynamo recorded replayed Python side effects for compiled code."""
    return bool(get_compiled_code_side_effects(code))

