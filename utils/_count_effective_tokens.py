from typing import Any, Dict, List, Optional, Union

def _count_effective_tokens(
    model: str,
    effective_messages: List[Dict[str, Any]],
    compaction_block: Optional[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]],
    system: Optional[Union[str, List[Dict[str, Any]]]] = None,
) -> int:
    """Token-count the conversation as it will appear downstream.

    The compaction block (if any) becomes a system prefix on the downstream
    call, so its content still counts even though it isn't in ``messages``.
    The system prompt (which may already include a prior compaction summary
    prepended via ``_augment_system_with_summary``) is also counted so the
    threshold check matches the downstream ``input_tokens`` metric.
    """
    # Local import to avoid pulling the adapter at module load time.
    from litellm.llms.anthropic.experimental_pass_through.adapters.transformation import (
        LiteLLMAnthropicMessagesAdapter,
    )

    messages_without_compaction = _strip_compaction_blocks(effective_messages)
    adapter = LiteLLMAnthropicMessagesAdapter()
    try:
        openai_shape = adapter.translate_anthropic_messages_to_openai(
            messages=cast(Any, messages_without_compaction)
        )
    except Exception as e:
        verbose_logger.debug(
            "compact_20260112: anthropic→openai translation failed during token "
            "count, falling back to raw messages: %s",
            e,
        )
        openai_shape = cast(Any, messages_without_compaction)

    # Translate Anthropic-shaped tools (``input_schema``) to OpenAI-shaped
    # tools (``{"type": "function", "function": {...}}``) so ``token_counter``
    # gets a consistent format regardless of which counting path it uses.
    # An inaccurate tool token count here could cause the polyfill to skip
    # needed compaction or trigger unnecessary summarization.
    openai_tools: Optional[List[Dict[str, Any]]] = None
    if tools:
        try:
            translated_tools, _ = adapter.translate_anthropic_tools_to_openai(
                tools=cast(Any, tools)
            )
            openai_tools = cast(List[Dict[str, Any]], translated_tools)
        except Exception as e:
            verbose_logger.debug(
                "compact_20260112: anthropic→openai tools translation failed "
                "during token count, falling back to raw tools: %s",
                e,
            )
            openai_tools = tools

    total = litellm.token_counter(
        model=model,
        messages=cast(Any, openai_shape),
        tools=cast(Any, openai_tools),
    )
    if compaction_block is not None:
        content = compaction_block.get("content") or ""
        if content:
            total += litellm.token_counter(model=model, text=content)
    system_text = _system_to_text(system)
    if system_text:
        total += litellm.token_counter(model=model, text=system_text)
    return total

