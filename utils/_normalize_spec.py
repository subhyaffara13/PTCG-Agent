
def _normalize_spec(
    spec: Union[Dict[str, Any], List[Dict[str, Any]], None],
) -> Optional[List[Dict[str, Any]]]:
    """Accept Anthropic-native dict form or OpenAI list form; return edits list."""
    if isinstance(spec, list):
        # Local import to avoid an import cycle at module load.
        from litellm.llms.anthropic.chat.transformation import AnthropicConfig

        spec = AnthropicConfig.map_openai_context_management_to_anthropic(spec)

    edits = spec.get("edits") if isinstance(spec, dict) else None
    if not edits or not isinstance(edits, list):
        return None
    return [edit for edit in edits if isinstance(edit, dict)]

