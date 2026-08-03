from typing import List

def _append_bedrock_tool_result_media_block(
    tool_result_content_blocks: List[BedrockToolResultContentBlock],
    processed_block: BedrockContentBlock,
    content: dict,
    content_type: str,
) -> None:
    if "image" in processed_block:
        tool_result_content_blocks.append(
            BedrockToolResultContentBlock(image=processed_block["image"])
        )
    elif "document" in processed_block:
        tool_result_content_blocks.append(
            BedrockToolResultContentBlock(document=processed_block["document"])
        )
    else:
        verbose_logger.warning(
            "Bedrock Converse: unrecognized BedrockContentBlock keys "
            "%s for %s tool-result block %s; dropping.",
            list(processed_block.keys()),
            content_type,
            content,
        )

