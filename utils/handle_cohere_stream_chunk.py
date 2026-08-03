import json
from typing import Any, Dict, List, Optional

def handle_cohere_stream_chunk(
    dict_chunk: dict,
    prior_tool_calls_emitted: bool = False,
    prior_text_emitted: bool = False,
) -> ModelResponseStream:
    """Parse a single Cohere SSE chunk into a LiteLLM ModelResponseStream.

    ``prior_tool_calls_emitted`` lets the caller signal whether tool calls
    were already emitted in earlier chunks of the same stream. When set, the
    terminal consolidation chunk's tool calls are suppressed (they would
    duplicate prior deltas); otherwise they are passed through so a stream
    that delivers tool calls only on the terminal chunk doesn't silently
    drop them.

    ``prior_text_emitted`` plays the analogous role for the ``text`` field:
    when set, the terminal consolidation chunk's ``text`` is suppressed
    (it would re-emit the full assembled response on top of prior deltas);
    when unset (e.g. a degenerate stream that delivers the entire response
    in a single SSE event carrying both ``chatHistory`` and ``finishReason``),
    the text is passed through so the response content isn't silently lost.
    """
    try:
        typed_chunk = CohereStreamChunk(**dict_chunk)
    except (TypeError, ValidationError) as e:
        raise OCIError(
            status_code=500,
            message=f"Chunk cannot be parsed as CohereStreamChunk: {str(e)}",
        )

    if typed_chunk.index is None:
        typed_chunk.index = 0

    # OCI Cohere's terminal SSE event re-sends the full assembled response in
    # `text` alongside a populated `chatHistory` and a non-null `finishReason`.
    # Emitting that text would concatenate the whole response onto the
    # already-streamed deltas. We require both signals to be present so that a
    # future API change which adds `chatHistory` to intermediate chunks (or a
    # rare early-populated case) doesn't silently drop legitimate token deltas.
    is_terminal_consolidation = (
        typed_chunk.chatHistory is not None and typed_chunk.finishReason is not None
    )
    # On non-terminal text-free chunks (e.g. tool-call-only or keep-alive
    # chunks) emit ``content=None`` rather than ``content=""`` so downstream
    # stream-mergers that distinguish "no text in this delta" from "an
    # explicitly empty text delta" behave correctly.
    #
    # We only suppress the terminal chunk's ``text`` when the caller has
    # confirmed that text deltas were already emitted earlier — otherwise
    # (e.g. a degenerate stream that delivers the whole response in a
    # single SSE event), passing it through is the only chance to surface it.
    text: Optional[str] = (
        None if (is_terminal_consolidation and prior_text_emitted) else typed_chunk.text
    )

    # Tool calls on the terminal consolidation chunk (whether from
    # `typed_chunk.toolCalls` or from `chatHistory`) typically restate what
    # was already streamed in intermediate chunks. Re-emitting them would
    # mint fresh `uuid4` IDs and cause downstream consumers to execute each
    # tool call twice. We only suppress when the caller has confirmed that
    # tool calls were already emitted earlier — otherwise (e.g. a short
    # response that delivers tool calls exclusively on the terminal chunk),
    # passing them through is the only chance to surface them.
    cohere_tool_calls = (
        None
        if (is_terminal_consolidation and prior_tool_calls_emitted)
        else typed_chunk.toolCalls
    )

    tool_calls: Optional[List[Dict[str, Any]]] = None
    if cohere_tool_calls:
        tool_calls = [
            {
                # Cohere protocol has no tool-call id, so we synthesize one
                # deterministically from the call's content/position. A random
                # uuid4 per chunk would cause downstream stream-mergers to
                # treat each chunk as a distinct tool call.
                "id": _synthesize_oci_tool_call_id(
                    i, tc.name, json.dumps(tc.parameters, sort_keys=True)
                ),
                "type": "function",
                "function": {
                    "name": tc.name,
                    "arguments": json.dumps(tc.parameters),
                },
            }
            for i, tc in enumerate(cohere_tool_calls)
        ]

    finish_reason = _normalize_oci_finish_reason(typed_chunk.finishReason)

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

