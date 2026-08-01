
def format_result(result: "mcp_types.CallToolResult") -> str:
    """
    Formats a mcp.types.CallToolResult content into a human-readable string.

    Args:
        result (CallToolResult)
            Object returned by mcp.ClientSession.call_tool.

    Returns:
        str
            A formatted string representing the content of the result.
    """
    content = result.content

    if len(content) == 0:
        return "[No content]"

    formatted_parts: list[str] = []

    for item in content:
        match item.type:
            case "text":
                formatted_parts.append(item.text)

            case "image":
                formatted_parts.append(
                    f"[Binary Content: Image {item.mimeType}, {_get_base64_size(item.data)} bytes]\n"
                    f"The task is complete and the content accessible to the User"
                )

            case "audio":
                formatted_parts.append(
                    f"[Binary Content: Audio {item.mimeType}, {_get_base64_size(item.data)} bytes]\n"
                    f"The task is complete and the content accessible to the User"
                )

            case "resource":
                resource = item.resource

                if hasattr(resource, "text") and isinstance(resource.text, str):
                    formatted_parts.append(resource.text)

                elif hasattr(resource, "blob") and isinstance(resource.blob, str):
                    formatted_parts.append(
                        f"[Binary Content ({resource.uri}): {resource.mimeType},"
                        f" {_get_base64_size(resource.blob)} bytes]\n"
                        f"The task is complete and the content accessible to the User"
                    )

    return "\n".join(formatted_parts)

