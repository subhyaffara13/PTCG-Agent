from typing import Union

def _anthropic_content_element_factory(
    image_chunk: GenericImageParsingChunk,
) -> Union[AnthropicMessagesImageParam, AnthropicMessagesDocumentParam]:
    if image_chunk["media_type"] == "application/pdf":
        _anthropic_content_element: Union[
            AnthropicMessagesDocumentParam, AnthropicMessagesImageParam
        ] = AnthropicMessagesDocumentParam(
            type="document",
            source=AnthropicContentParamSource(
                type="base64",
                media_type=image_chunk["media_type"],
                data=image_chunk["data"],
            ),
        )
    else:
        _anthropic_content_element = AnthropicMessagesImageParam(
            type="image",
            source=AnthropicContentParamSource(
                type="base64",
                media_type=image_chunk["media_type"],
                data=image_chunk["data"],
            ),
        )

    return _anthropic_content_element

