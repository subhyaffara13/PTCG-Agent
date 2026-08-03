from typing import Any, Dict, List, Optional

def handle_generic_stream_chunk(dict_chunk: dict) -> ModelResponseStream:
    """Parse a single GENERIC SSE chunk into a LiteLLM ModelResponseStream."""
    # OCI streams tool calls progressively — early chunks may omit required fields.
    if dict_chunk.get("message") and dict_chunk["message"].get("toolCalls"):
        for tool_call in dict_chunk["message"]["toolCalls"]:
            tool_call.setdefault("arguments", "")
            tool_call.setdefault("id", "")
            tool_call.setdefault("name", "")

    try:
        typed_chunk = OCIStreamChunk(**dict_chunk)
    except (TypeError, ValidationError) as e:
        raise OCIError(
            status_code=500,
            message=f"Chunk cannot be parsed as OCIStreamChunk: {str(e)}",
        )

    if typed_chunk.index is None:
        typed_chunk.index = 0

    # Emit ``content=None`` rather than ``content=""`` on chunks with no text
    # parts (e.g. tool-call-only or keep-alive chunks) so downstream
    # stream-mergers that distinguish "no text in this delta" from "an
    # explicitly empty text delta" behave correctly.
    text: Optional[str] = None
    if typed_chunk.message and typed_chunk.message.content:
        for item in typed_chunk.message.content:
            if isinstance(item, OCITextContentPart):
                text = (text or "") + item.text
            elif isinstance(item, OCIImageContentPart):
                raise OCIError(
                    status_code=500,
                    message="OCI returned image content in a streaming response — not supported",
                )
            else:
                raise OCIError(
                    status_code=500,
                    message=f"Unsupported content type in OCI streaming response: {item.type}",
                )

    # Build plain tool-call dicts inline (matching the shape produced by
    # ``handle_cohere_stream_chunk``) rather than calling
    # ``adapt_tools_to_openai_standard`` and ``model_dump``-ing the typed
    # objects. Both code paths feed ``Delta.tool_calls``, so emitting the
    # same minimal ``{"id", "type", "function": {"name", "arguments"}}``
    # shape keeps downstream stream-mergers behaving identically across
    # GENERIC and Cohere chunks.
    tool_calls: Optional[List[Dict[str, Any]]] = None
    if typed_chunk.message and typed_chunk.message.toolCalls:
        tool_calls = [
            {
                "id": tc.id or _synthesize_oci_tool_call_id(i, tc.name, tc.arguments),
                "type": "function",
                "function": {
                    "name": tc.name,
                    "arguments": tc.arguments,
                },
            }
            for i, tc in enumerate(typed_chunk.message.toolCalls)
        ]

    finish_reason: Optional[str] = _normalize_oci_finish_reason(
        typed_chunk.finishReason
    )

    return ModelResponseStream(
        choices=[
            StreamingChoices(
                index=typed_chunk.index,
                delta=Delta(
                    content=text,
                    tool_calls=tool_calls,
                    provider_specific_fields=None,
                    thinking_blocks=None,
                    reasoning_content=None,
                ),
                finish_reason=finish_reason,
            )
        ]
    )

