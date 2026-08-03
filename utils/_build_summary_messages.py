from typing import Any, Dict, List, Optional, Union

def _build_summary_messages(
    effective_messages: List[Dict[str, Any]],
    prompt: str,
    system: Optional[Union[str, List[Dict[str, Any]]]] = None,
) -> List[Dict[str, Any]]:
    """Build the OpenAI-shape message list for the summary call.

    The caller's ``system`` prompt is prepended (the default summarization
    instructions reference "the initial task above", which lives in that
    system prompt); the conversation history is translated to OpenAI shape;
    the summarization prompt is appended as a final user turn.
    """
    from litellm.llms.anthropic.experimental_pass_through.adapters.transformation import (
        LiteLLMAnthropicMessagesAdapter,
    )

    stripped = _strip_compaction_blocks(effective_messages)
    try:
        openai_messages = (
            LiteLLMAnthropicMessagesAdapter().translate_anthropic_messages_to_openai(
                messages=cast(Any, stripped)
            )
        )
    except Exception as e:
        verbose_logger.warning(
            "compact_20260112: anthropic→openai translation failed when "
            "building summary call; falling back to raw shape: %s",
            e,
        )
        openai_messages = cast(Any, stripped)

    summary_messages: List[Dict[str, Any]] = []
    system_message = _system_to_openai_message(system)
    if system_message is not None:
        summary_messages.append(system_message)
    summary_messages.extend(openai_messages)
    # If the last turn is already a user message, merge the summarization
    # prompt into it. Some providers (and strict OpenAI-compatible endpoints)
    # reject two consecutive ``role=user`` messages, which would otherwise
    # silently fall into the ``summary_call_failed`` error path.
    if summary_messages and _is_user_message(summary_messages[-1]):
        last_msg = summary_messages[-1]
        summary_messages[-1] = {
            **last_msg,
            "content": _append_text_to_content(last_msg.get("content"), prompt),
        }
    else:
        summary_messages.append({"role": "user", "content": prompt})
    return summary_messages

