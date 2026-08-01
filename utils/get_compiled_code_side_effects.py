
def get_compiled_code_side_effects(
    code: types.CodeType,
) -> tuple[str, ...] | None:
    """Return Dynamo's replayed Python side-effect sources for compiled code.

    Returns ``None`` when ``code`` was not produced by Dynamo or no metadata was
    attached to it.
    """
    if not code_context.has_context(code):
        return None
    side_effects = code_context.get_context(code).get(
        _BYTECODE_HOOK_SIDE_EFFECTS_CONTEXT_KEY
    )
    if side_effects is None:
        return None
    return side_effects

