
def _set_usage_outputs(span: "Span", response_obj, span_attrs):
    usage = response_obj and response_obj.get("usage")
    if not usage:
        return

    safe_set_attribute(
        span, span_attrs.LLM_TOKEN_COUNT_TOTAL, _safe_get(usage, "total_tokens")
    )
    completion_tokens = _safe_get(usage, "completion_tokens") or _safe_get(
        usage, "output_tokens"
    )
    if completion_tokens:
        safe_set_attribute(
            span, span_attrs.LLM_TOKEN_COUNT_COMPLETION, completion_tokens
        )
    prompt_tokens = _safe_get(usage, "prompt_tokens") or _safe_get(
        usage, "input_tokens"
    )
    if prompt_tokens:
        safe_set_attribute(span, span_attrs.LLM_TOKEN_COUNT_PROMPT, prompt_tokens)

    # Reasoning tokens live in `completion_tokens_details` for Chat Completions
    # API (Usage) and in `output_tokens_details` for Responses API
    # (ResponseAPIUsage). Both nested objects may be plain Pydantic models
    # without `.get`.
    token_details = _safe_get(usage, "completion_tokens_details") or _safe_get(
        usage, "output_tokens_details"
    )
    reasoning_tokens = _safe_get(token_details, "reasoning_tokens")
    if reasoning_tokens:
        safe_set_attribute(
            span,
            span_attrs.LLM_TOKEN_COUNT_COMPLETION_DETAILS_REASONING,
            reasoning_tokens,
        )

    # Additive: cache token breakdown so prompt-caching savings render in
    # Arize. Sources covered:
    #   - OpenAI Chat Completions: `prompt_tokens_details.cached_tokens`
    #   - Anthropic / Bedrock-Anthropic: `cache_read_input_tokens`,
    #     `cache_creation_input_tokens`
    # All emits are conditional, so when none of these fields exist (the
    # situation in the existing test fixtures) no extra attributes are set.
    prompt_token_details = _safe_get(usage, "prompt_tokens_details") or _safe_get(
        usage, "input_tokens_details"
    )
    cache_read = _safe_get(prompt_token_details, "cached_tokens") or _safe_get(
        usage, "cache_read_input_tokens"
    )
    if cache_read:
        safe_set_attribute(
            span,
            span_attrs.LLM_TOKEN_COUNT_PROMPT_DETAILS_CACHE_READ,
            cache_read,
        )
    # Anthropic / Bedrock-Anthropic only — OpenAI's `prompt_tokens_details`
    # does not expose a cache-write count, so we read straight off `usage`.
    cache_write = _safe_get(usage, "cache_creation_input_tokens")
    if cache_write:
        safe_set_attribute(
            span,
            span_attrs.LLM_TOKEN_COUNT_PROMPT_DETAILS_CACHE_WRITE,
            cache_write,
        )

    audio_prompt_tokens = _safe_get(prompt_token_details, "audio_tokens")
    if audio_prompt_tokens:
        safe_set_attribute(
            span,
            span_attrs.LLM_TOKEN_COUNT_PROMPT_DETAILS_AUDIO,
            audio_prompt_tokens,
        )

