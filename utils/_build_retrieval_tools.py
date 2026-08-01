
def _build_retrieval_tools(keys: List[str], call_type: str) -> List[dict]:
    """
    Build retrieval tool definitions in the target request schema.

    - Chat-completions call types: keep OpenAI function-tool schema.
    - Anthropic messages call type: remap to Anthropic's custom tool schema.
    """
    if not keys:
        return []

    openai_tools = [build_retrieval_tool(keys)]
    if not _is_anthropic_call_type(call_type):
        return openai_tools

    # Lazy import to avoid introducing provider transformation imports during
    # module import for non-Anthropic call paths.
    from litellm.llms.anthropic.chat.transformation import AnthropicConfig

    anthropic_tools, _mcp_servers = AnthropicConfig()._map_tools(openai_tools)
    return cast(List[dict], anthropic_tools)

