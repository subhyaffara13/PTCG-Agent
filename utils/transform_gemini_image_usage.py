
def transform_gemini_image_usage(usage_metadata: dict) -> ImageUsage:
    """
    Transform Gemini usageMetadata to ImageUsage format.
    """
    input_tokens_details = _sum_modality_token_details(
        usage_metadata, "promptTokensDetails", "prompt_tokens_details"
    )
    output_tokens = usage_metadata.get("candidatesTokenCount", 0)
    output_tokens_details = _sum_modality_token_details(
        usage_metadata, "candidatesTokensDetails", "candidates_tokens_details"
    )

    if not _get_modality_token_details(
        usage_metadata, "candidatesTokensDetails", "candidates_tokens_details"
    ):
        output_tokens_details.image_tokens = output_tokens
    else:
        known_output_tokens = (
            output_tokens_details.text_tokens + output_tokens_details.image_tokens
        )
        if output_tokens > known_output_tokens:
            output_tokens_details.text_tokens += output_tokens - known_output_tokens

    usage_payload: dict[str, Any] = {
        "input_tokens": usage_metadata.get("promptTokenCount", 0),
        "input_tokens_details": input_tokens_details,
        "output_tokens": output_tokens,
        "total_tokens": usage_metadata.get("totalTokenCount", 0),
        "prompt_tokens": usage_metadata.get("promptTokenCount", 0),
        "prompt_tokens_details": input_tokens_details.model_dump(),
        "completion_tokens": output_tokens,
        "completion_tokens_details": output_tokens_details.model_dump(),
        "output_tokens_details": output_tokens_details.model_dump(),
    }
    return ImageUsage(**usage_payload)

