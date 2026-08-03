from typing import List

def _deduplicate_bedrock_tool_content(
    tool_content: List[BedrockContentBlock],
) -> List[BedrockContentBlock]:
    """Convenience wrapper: deduplicate ``toolResult`` blocks by ``toolUseId``."""
    return _deduplicate_bedrock_content_blocks(tool_content, "toolResult")

