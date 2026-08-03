from typing import List, Optional

def is_prompt_caching_valid_prompt(
    model: str,
    messages: Optional[List[AllMessageValues]],
    tools: Optional[List[ChatCompletionToolParam]] = None,
    custom_llm_provider: Optional[str] = None,
) -> bool:
    """
    Returns true if the prompt is valid for prompt caching.

    OpenAI + Anthropic providers have a minimum token count of 1024 for prompt caching.
    """
    try:
        if messages is None and tools is None:
            return False
        if custom_llm_provider is not None and not model.startswith(
            custom_llm_provider
        ):
            model = custom_llm_provider + "/" + model
        token_count = token_counter(
            messages=messages,
            tools=tools,
            model=model,
            use_default_image_token_count=True,
        )
        return token_count >= MINIMUM_PROMPT_CACHE_TOKEN_COUNT
    except Exception as e:
        verbose_logger.error(f"Error in is_prompt_caching_valid_prompt: {e}")
        return False

