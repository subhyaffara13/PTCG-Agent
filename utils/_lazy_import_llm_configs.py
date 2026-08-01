
def _lazy_import_llm_configs(name: str) -> Any:
    """Handler for LLM config classes (AnthropicConfig, OpenAILikeChatConfig, etc.)"""
    return _generic_lazy_import(name, _LLM_CONFIGS_IMPORT_MAP, "LLM config")

