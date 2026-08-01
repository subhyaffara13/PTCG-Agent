
def get_tool_search_beta_header(custom_llm_provider: str) -> str:
    """
    Get the tool search beta header for a given provider.
    """
    return TOOL_SEARCH_BETA_HEADER_BY_PROVIDER.get(
        custom_llm_provider, TOOL_SEARCH_BETA_HEADER_ANTHROPIC
    )

