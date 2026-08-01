
def create_anthropic_image_param(
    image_url_input: Union[str, dict],
    format: Optional[str] = None,
    is_bedrock_invoke: bool = False,
) -> AnthropicMessagesImageParam:
    """
    Create an AnthropicMessagesImageParam from an image URL input.

    Supports both URL references (for HTTP/HTTPS URLs) and base64 encoding.
    """
    # Extract URL and format from input
    if isinstance(image_url_input, str):
        image_url = image_url_input
    else:
        image_url = image_url_input.get("url", "")
        if format is None:
            format = image_url_input.get("format")

    # Check if the image URL is an HTTP/HTTPS URL
    if image_url.startswith("http://") or image_url.startswith("https://"):
        # For Bedrock invoke and Vertex AI Anthropic, always convert URLs to base64
        # as these providers don't support URL sources for images
        if is_bedrock_invoke or image_url.startswith("http://"):
            base64_url = convert_url_to_base64(url=image_url)
            image_chunk = convert_to_anthropic_image_obj(
                openai_image_url=base64_url, format=format
            )
            return AnthropicMessagesImageParam(
                type="image",
                source=AnthropicContentParamSource(
                    type="base64",
                    media_type=image_chunk["media_type"],
                    data=image_chunk["data"],
                ),
            )
        else:
            # HTTPS URL - pass directly for regular Anthropic
            return AnthropicMessagesImageParam(
                type="image",
                source=AnthropicContentParamSourceUrl(
                    type="url",
                    url=image_url,
                ),
            )
    else:
        # Convert to base64 for data URIs or other formats
        image_chunk = convert_to_anthropic_image_obj(
            openai_image_url=image_url, format=format
        )
        return AnthropicMessagesImageParam(
            type="image",
            source=AnthropicContentParamSource(
                type="base64",
                media_type=image_chunk["media_type"],
                data=image_chunk["data"],
            ),
        )

