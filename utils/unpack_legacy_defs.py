import copy

def unpack_legacy_defs(
    schema: dict,
    *,
    copy: bool = False,
    max_inlined_bytes: int = _LEGACY_DEFS_MAX_INLINED_BYTES,
) -> dict:
    """Inline ``$ref``s backed by draft-04 ``definitions`` / OpenAPI
    ``components.schemas``. ``$defs`` is left untouched.

    Anthropic and Fireworks tool-schema resolvers only recognise ``$defs``;
    legacy / OpenAPI def blocks are otherwise silently dropped and leave
    dangling pointers. See https://github.com/BerriAI/litellm/issues/26692.

    Mutates ``schema`` in place and returns it. Pass ``copy=True`` to deep-copy
    first (only when there is actually work to do). ``max_inlined_bytes``
    bounds the cumulative JSON-byte size of inlined targets so request-supplied
    schemas cannot expand into a schema-bomb before reaching the upstream
    provider -- raises ``ValueError`` on overflow.
    """
    if not _has_legacy_defs(schema):
        return schema
    if copy:
        import copy as _copy

        schema = _copy.deepcopy(schema)
    # On key collision, ``definitions`` wins over ``components.schemas`` --
    # ``unpack_defs`` keys refs by last path segment so a single name can only
    # resolve to one body, and ``definitions`` is the JSON-Schema-native
    # namespace.
    defs = schema.pop("components", {}).get("schemas") or {}
    defs.update(schema.pop("definitions", None) or {})
    unpack_defs(schema, defs, max_inlined_bytes=max_inlined_bytes)
    return schema

