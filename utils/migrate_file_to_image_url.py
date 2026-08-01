
def migrate_file_to_image_url(
    message: "ChatCompletionFileObject",
) -> "ChatCompletionImageObject":
    """
    Migrate file to image_url
    """
    from litellm.types.llms.openai import (
        ChatCompletionImageObject,
        ChatCompletionImageUrlObject,
    )

    file_sub = message.get("file")
    if file_sub is None:
        raise litellm.BadRequestError(
            message="Content block has type='file' but is missing the required 'file' field",
            model=None,
            llm_provider=None,
        )
    file_id = file_sub.get("file_id")
    file_data = file_sub.get("file_data")
    format = file_sub.get("format")
    if not file_id and not file_data:
        raise ValueError("file_id and file_data are both None")
    image_url_object = ChatCompletionImageObject(
        type="image_url",
        image_url=ChatCompletionImageUrlObject(
            url=cast(str, file_id or file_data),
        ),
    )
    if format and isinstance(image_url_object["image_url"], dict):
        image_url_object["image_url"]["format"] = format
    return image_url_object

