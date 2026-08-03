import json
from typing import Any, Dict, List, Optional

def handle_cohere_response(
    json_response: dict,
    model: str,
    model_response: ModelResponse,
    raw_response: httpx.Response,
) -> ModelResponse:
    """Parse a non-streaming Cohere OCI response into a LiteLLM ModelResponse."""
    try:
        cohere_response = CohereChatResult(**json_response)
    except (TypeError, ValidationError) as e:
        raise OCIError(
            message=f"Response cannot be casted to CohereChatResult: {str(e)}",
            status_code=raw_response.status_code,
        )

    model_response.model = model
    model_response.created = int(datetime.datetime.now().timestamp())

    response_text = cohere_response.chatResponse.text
    finish_reason = _normalize_oci_finish_reason(
        cohere_response.chatResponse.finishReason
    )

    tool_calls: Optional[List[Dict[str, Any]]] = None
    if cohere_response.chatResponse.toolCalls:
        tool_calls = [
            {
                "id": _synthesize_oci_tool_call_id(
                    i, tc.name, json.dumps(tc.parameters, sort_keys=True)
                ),
                "type": "function",
                "function": {
                    "name": tc.name,
                    "arguments": json.dumps(tc.parameters),
                },
            }
            for i, tc in enumerate(cohere_response.chatResponse.toolCalls)
        ]

    content: Optional[str] = response_text if response_text else None

    # Only include ``tool_calls`` in the message dict when actually present.
    # Passing an explicit ``None`` would let downstream consumers that key off
    # ``"tool_calls" in message`` (rather than truthiness) incorrectly conclude
    # that tool calls were attempted. Matches the generic handler's behaviour,
    # which only sets ``message.tool_calls`` when tool calls are present.
    message: Dict[str, Any] = {"role": "assistant", "content": content}
    if tool_calls is not None:
        message["tool_calls"] = tool_calls

    model_response.choices = [
        Choices(
            index=0,
            message=message,
            finish_reason=finish_reason,
        )
    ]

    usage_info = cohere_response.chatResponse.usage
    if usage_info is not None:
        model_response.usage = Usage(  # type: ignore[attr-defined]
            prompt_tokens=usage_info.promptTokens,
            completion_tokens=usage_info.completionTokens,
            total_tokens=usage_info.totalTokens,
        )
    else:
        model_response.usage = Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0)  # type: ignore[attr-defined]

    return model_response

