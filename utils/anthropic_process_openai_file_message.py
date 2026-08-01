
def anthropic_process_openai_file_message(
    message: ChatCompletionFileObject,
) -> Union[
    AnthropicMessagesDocumentParam,
    AnthropicMessagesImageParam,
    AnthropicMessagesContainerUploadParam,
]:
    file_message = cast(ChatCompletionFileObject, message)
    file_sub = file_message.get("file")
    if file_sub is None:
        raise litellm.BadRequestError(
            message="Content block has type='file' but is missing the required 'file' field",
            model=None,
            llm_provider="anthropic",
        )
    file_data = file_sub.get("file_data")
    file_id = file_sub.get("file_id")
    format = file_sub.get("format")
    if file_data:
        image_chunk = convert_to_anthropic_image_obj(
            openai_image_url=file_data,
            format=format,
        )
        anthropic_document_param = AnthropicMessagesDocumentParam(
            type="document",
            source=AnthropicContentParamSource(
                type="base64",
                media_type=image_chunk["media_type"],
                data=image_chunk["data"],
            ),
        )
        return anthropic_document_param
    elif file_id:
        content_block_type = (
            select_anthropic_content_block_type_for_file(format)
            if format
            else anthropic_infer_file_id_content_type(file_id)
        )
        return_block_param: Optional[
            Union[
                AnthropicMessagesDocumentParam,
                AnthropicMessagesImageParam,
                AnthropicMessagesContainerUploadParam,
            ]
        ] = None
        if content_block_type == "document":
            return_block_param = AnthropicMessagesDocumentParam(
                type="document",
                source=AnthropicContentParamSourceFileId(
                    type="file",
                    file_id=file_id,
                ),
            )
        elif content_block_type == "document_url":
            return_block_param = AnthropicMessagesDocumentParam(
                type="document",
                source=AnthropicContentParamSourceUrl(
                    type="url",
                    url=file_id,
                ),
            )
        elif content_block_type == "image":
            return_block_param = AnthropicMessagesImageParam(
                type="image",
                source=AnthropicContentParamSourceFileId(
                    type="file",
                    file_id=file_id,
                ),
            )
        elif content_block_type == "container_upload":
            return_block_param = AnthropicMessagesContainerUploadParam(
                type="container_upload", file_id=file_id
            )

        if return_block_param is None:
            raise Exception(f"Unable to parse anthropic file message: {message}")
        return return_block_param
    raise Exception(
        f"Either file_data or file_id must be present in the file message: {message}"
    )

