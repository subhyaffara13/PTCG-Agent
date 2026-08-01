
def _system_to_openai_message(
    system: Optional[Union[str, List[Dict[str, Any]]]],
) -> Optional[Dict[str, Any]]:
    """Translate Anthropic-shaped ``system`` to an OpenAI system message.

    Accepts a bare string or a list of Anthropic content blocks; returns
    ``None`` if no usable text is present. Only ``type=="text"`` blocks are
    carried over — the summary model has no use for ``cache_control`` or
    other non-text metadata.
    """
    if isinstance(system, str):
        return {"role": "system", "content": system} if system else None
    if isinstance(system, list):
        parts = [
            block.get("text", "")
            for block in system
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        joined = "\n\n".join(part for part in parts if part)
        return {"role": "system", "content": joined} if joined else None
    return None

