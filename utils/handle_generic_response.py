
def handle_generic_response(
    json_data: dict,
    model: str,
    model_response: ModelResponse,
    raw_response: httpx.Response,
) -> ModelResponse:
    """Parse a non-streaming GENERIC OCI response into a LiteLLM ModelResponse."""
    try:
        completion_response = OCICompletionResponse(**json_data)
    except (TypeError, ValidationError) as e:
        raise OCIError(
            message=f"Response cannot be casted to OCICompletionResponse: {str(e)}",
            status_code=raw_response.status_code,
        )

    iso_str = completion_response.chatResponse.timeCreated
    dt = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    model_response.created = int(dt.timestamp())
    model_response.model = completion_response.modelId

    if not completion_response.chatResponse.choices:
        raise OCIError(
            message="OCI response contained no choices",
            status_code=raw_response.status_code,
        )

    response_choice = completion_response.chatResponse.choices[0]
    message = model_response.choices[0].message  # type: ignore
    response_message = response_choice.message
    if response_message is not None:
        if response_message.content:
            # Concatenate all text parts — matches the streaming handler, which
            # iterates the full content array. Skips non-text parts (e.g. image
            # parts) so a leading non-text part doesn't suppress trailing text.
            text: Optional[str] = None
            for item in response_message.content:
                if isinstance(item, OCITextContentPart):
                    text = (text or "") + item.text
            if text is not None:
                message.content = text
        if response_message.toolCalls:
            message.tool_calls = adapt_tools_to_openai_standard(
                response_message.toolCalls
            )

    model_response.choices[0].finish_reason = _normalize_oci_finish_reason(  # type: ignore[union-attr,assignment]
        response_choice.finishReason
    )

    oci_usage = completion_response.chatResponse.usage
    reasoning_tokens: Optional[int] = None
    if (
        oci_usage.completionTokensDetails
        and oci_usage.completionTokensDetails.reasoningTokens is not None
    ):
        reasoning_tokens = oci_usage.completionTokensDetails.reasoningTokens
    model_response.usage = Usage(  # type: ignore[attr-defined]
        prompt_tokens=oci_usage.promptTokens,
        completion_tokens=oci_usage.completionTokens or 0,
        total_tokens=oci_usage.totalTokens,
        reasoning_tokens=reasoning_tokens,
    )

    return model_response

