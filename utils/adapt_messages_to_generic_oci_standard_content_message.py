from typing import List, Union

def adapt_messages_to_generic_oci_standard_content_message(
    role: str, content: Union[str, list]
) -> OCIMessage:
    """Convert a plain-text or multipart content message to OCI format."""
    new_content: List[OCIContentPartUnion] = []
    if isinstance(content, str):
        return OCIMessage(
            role=open_ai_to_generic_oci_role_map[role],
            content=[OCITextContentPart(text=content)],
            toolCalls=None,
            toolCallId=None,
        )

    for content_item in content:
        if not isinstance(content_item, dict):
            raise OCIError(
                status_code=400, message="Each content item must be a dictionary"
            )

        item_type = content_item.get("type")
        if not isinstance(item_type, str):
            raise OCIError(
                status_code=400,
                message="Each content item must have a string `type` field",
            )
        if item_type not in ["text", "image_url"]:
            raise OCIError(
                status_code=400,
                message=f"Content type `{item_type}` is not supported by OCI",
            )

        if item_type == "text":
            text = content_item.get("text")
            if not isinstance(text, str):
                raise OCIError(
                    status_code=400,
                    message="Content item of type `text` must have a string `text` field",
                )
            new_content.append(OCITextContentPart(text=text))

        elif item_type == "image_url":
            image_url = content_item.get("image_url")
            if isinstance(image_url, dict):
                image_url = image_url.get("url")
            if not isinstance(image_url, str):
                raise OCIError(
                    status_code=400,
                    message="Prop `image_url` must be a string or an object with a `url` property",
                )
            new_content.append(OCIImageContentPart(imageUrl=OCIImageUrl(url=image_url)))

    return OCIMessage(
        role=open_ai_to_generic_oci_role_map[role],
        content=new_content,
        toolCalls=None,
        toolCallId=None,
    )

