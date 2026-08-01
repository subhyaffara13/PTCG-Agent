
def _spec_has_non_compact_edits(
    *,
    context_management_spec: Any,
    drop_params: Optional[bool],
) -> bool:
    """Return True when the spec includes edits other than ``compact_20260112``.

    Used to decide whether a polyfill failure can be silently swallowed
    (compact-only specs have a safe compaction-block slicing fallback) or
    must be surfaced (other editors like ``clear_tool_uses_20250919`` have
    no slice-only fallback and would otherwise be dropped without notice).
    """
    edits = _normalize_spec_edits(
        context_management_spec=context_management_spec,
        drop_params=drop_params,
    )
    if edits is None:
        return False

    from litellm.llms.anthropic.experimental_pass_through.context_management.constants import (
        COMPACT_EDIT_TYPE,
    )

    return any(
        isinstance(edit, dict)
        and isinstance(edit.get("type"), str)
        and edit.get("type") != COMPACT_EDIT_TYPE
        for edit in edits
    )

