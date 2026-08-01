
def _parse_bedrock_tool_result_content_list(
    content_list: List,
) -> List[BedrockToolResultContentBlock]:
    tool_result_content_blocks: List[BedrockToolResultContentBlock] = []
    for content in content_list:
        if content["type"] == "text":
            tool_result_content_blocks.append(
                BedrockToolResultContentBlock(text=content["text"])
            )
        elif content["type"] == "image_url":
            _append_bedrock_tool_result_image_url_block(
                tool_result_content_blocks, content
            )
        elif content["type"] == "file":
            _append_bedrock_tool_result_file_block(tool_result_content_blocks, content)
    return tool_result_content_blocks

