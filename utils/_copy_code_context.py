
def _copy_code_context(src_code: types.CodeType, dst_code: types.CodeType) -> None:
    if not code_context.has_context(src_code):
        return
    src_context = code_context.get_context(src_code)
    if _BYTECODE_HOOK_SIDE_EFFECTS_CONTEXT_KEY in src_context:
        code_context.get_context(dst_code)[_BYTECODE_HOOK_SIDE_EFFECTS_CONTEXT_KEY] = (
            src_context[_BYTECODE_HOOK_SIDE_EFFECTS_CONTEXT_KEY]
        )

