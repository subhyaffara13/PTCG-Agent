
def _append_bedrock_tool_result_file_block(
    tool_result_content_blocks: List[BedrockToolResultContentBlock],
    content: dict,
) -> None:
    # Match the user-message path (_process_file_message): accept either
    # file_data (base64 data URI) or file_id (server-side reference / URL).
    file_obj = content.get("file") or {}
    file_data = file_obj.get("file_data")
    file_id = file_obj.get("file_id")
    if file_data is None and file_id is None:
        raise litellm.BadRequestError(
            message="file_data and file_id cannot both be None. Got={}".format(content),
            model="",
            llm_provider="bedrock",
        )
    processed_block = BedrockImageProcessor.process_image_sync(
        image_url=cast(str, file_id or file_data),
        format=file_obj.get("format"),
    )
    _append_bedrock_tool_result_media_block(
        tool_result_content_blocks, processed_block, content, "file"
    )

