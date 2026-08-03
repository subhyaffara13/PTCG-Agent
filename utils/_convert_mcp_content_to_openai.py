from typing import Any, Dict, List, Union

def _convert_mcp_content_to_openai(
    content: Any,
) -> Union[str, Dict[str, Any], List[Dict[str, Any]]]:
    """
    Convert MCP SamplingMessage content to OpenAI message content format.
    Handles:
    - TextContent → string or {"type": "text", "text": ...}
    - ImageContent → {"type": "image_url", "image_url": {"url": "data:..."}}
    - AudioContent → {"type": "input_audio", "input_audio": {...}}
    - ToolUseContent → function call representation
    - ToolResultContent → tool result representation
    - List of mixed content → list of content parts
    """
    if isinstance(content, list):
        parts = []
        for item in content:
            converted = _convert_single_content(item)
            if isinstance(converted, list):
                parts.extend(converted)
            else:
                parts.append(converted)
        return parts
    return _convert_single_content(content)

