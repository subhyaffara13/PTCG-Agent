from typing import List, Optional

def _append_bedrock_tool_result_image_url_block(
    tool_result_content_blocks: List[BedrockToolResultContentBlock],
    content: dict,
) -> None:
    format: Optional[str] = None
    if isinstance(content["image_url"], dict):
        image_url = content["image_url"]["url"]
        format = content["image_url"].get("format")
    else:
        image_url = content["image_url"]
    processed_block = BedrockImageProcessor.process_image_sync(
        image_url=image_url,
        format=format,
    )
    _append_bedrock_tool_result_media_block(
        tool_result_content_blocks, processed_block, content, "image_url"
    )

