from typing import Optional

def _encode_tool_call_id_with_signature(
    tool_call_id: str, thought_signature: Optional[str]
) -> str:
    """
    Embed thought signature into tool call ID for OpenAI client compatibility.

    Args:
        tool_call_id: The tool call ID (e.g., "call_abc123...")
        thought_signature: Base64-encoded signature from Gemini response

    Returns:
        Tool call ID with embedded signature if present, otherwise original ID
        Format: call_<uuid>__thought__<base64_signature>

    See: https://ai.google.dev/gemini-api/docs/thought-signatures
    """
    if thought_signature:
        return f"{tool_call_id}{THOUGHT_SIGNATURE_SEPARATOR}{thought_signature}"
    return tool_call_id

