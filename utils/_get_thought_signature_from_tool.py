
def _get_thought_signature_from_tool(
    tool: dict, model: Optional[str] = None
) -> Optional[str]:
    """Extract thought signature from tool call's provider_specific_fields.

    If not provided try to extract thought signature from tool call id

    Checks both tool.provider_specific_fields and tool.function.provider_specific_fields.
    If no signature is found and model is gemini-3, returns a dummy signature.
    """
    # First check tool's provider_specific_fields
    provider_fields = tool.get("provider_specific_fields") or {}
    if isinstance(provider_fields, dict):
        signature = provider_fields.get("thought_signature")
        if signature:
            return signature

    # Then check function's provider_specific_fields
    function = tool.get("function")
    if function:
        if isinstance(function, dict):
            func_provider_fields = function.get("provider_specific_fields") or {}
            if isinstance(func_provider_fields, dict):
                signature = func_provider_fields.get("thought_signature")
                if signature:
                    return signature
        elif (
            hasattr(function, "provider_specific_fields")
            and function.provider_specific_fields
        ):
            if isinstance(function.provider_specific_fields, dict):
                signature = function.provider_specific_fields.get("thought_signature")
                if signature:
                    return signature
    # Check if thought signature is embedded in tool call ID
    tool_call_id = tool.get("id")
    if tool_call_id and THOUGHT_SIGNATURE_SEPARATOR in tool_call_id:
        parts = tool_call_id.split(THOUGHT_SIGNATURE_SEPARATOR, 1)
        if len(parts) == 2:
            _, signature = parts
            return signature
    # If no signature found and model is gemini-3, return dummy signature
    from litellm.llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import (
        VertexGeminiConfig,
    )

    if model and VertexGeminiConfig._is_gemini_3_or_newer(model):
        return _get_dummy_thought_signature()
    return None

