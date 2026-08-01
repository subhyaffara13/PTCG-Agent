
def _extract_tool_results(content: Any) -> List[Dict[str, Any]]:
    """Extract OpenAI-format tool messages from MCP ToolResultContent."""
    items = content if isinstance(content, list) else [content]
    results = []
    for item in items:
        if getattr(item, "type", None) == "tool_result":
            tool_use_id = getattr(item, "toolUseId", "")
            # Extract text from nested content
            nested_content = getattr(item, "content", [])
            if isinstance(nested_content, list):
                text_parts = [
                    getattr(c, "text", str(c))
                    for c in nested_content
                    if getattr(c, "type", None) == "text"
                ]
                result_text = "\n".join(text_parts) if text_parts else ""
            else:
                result_text = str(nested_content)
            results.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_use_id,
                    "content": result_text,
                }
            )
    return results

