
def _wrap_editor_return(raw: Any, *, fallback_system: Any) -> PolyfillResult:
    """Coerce an editor's native return shape into a ``PolyfillResult``.

    v0 sync editors (e.g. ``clear_tool_uses_20250919``) return a 2-tuple
    ``(messages, Optional[AppliedEdit])``. The new async ``compact_20260112``
    editor returns a ``PolyfillResult`` directly.
    """
    if isinstance(raw, PolyfillResult):
        return raw
    # Legacy 2-tuple return — sync editors don't mutate ``system``, so
    # carry the caller's value forward.
    messages, applied = cast(Tuple[List[Dict[str, Any]], Any], raw)
    return PolyfillResult(
        messages=messages,
        system=fallback_system,
        applied_edits=[applied] if applied is not None else [],
    )

