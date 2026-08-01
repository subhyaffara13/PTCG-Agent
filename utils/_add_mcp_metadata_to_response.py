
def _add_mcp_metadata_to_response(
    response: Union[ModelResponse, CustomStreamWrapper],
    openai_tools: Optional[List],
    tool_calls: Optional[List] = None,
    tool_results: Optional[List] = None,
) -> None:
    """
    Add MCP metadata to response's provider_specific_fields.

    This function adds MCP-related information to the response so that
    clients can access which tools were available, which were called, and
    what results were returned.

    For ModelResponse: adds to choices[].message.provider_specific_fields
    For CustomStreamWrapper: stores in _hidden_params and automatically adds to
    final chunk's delta.provider_specific_fields via CustomStreamWrapper._add_mcp_metadata_to_final_chunk()
    """
    if isinstance(response, CustomStreamWrapper):
        # For streaming, store MCP metadata in _hidden_params
        # CustomStreamWrapper._add_mcp_metadata_to_final_chunk() will automatically
        # add it to the final chunk's delta.provider_specific_fields
        if not hasattr(response, "_hidden_params"):
            response._hidden_params = {}

        mcp_metadata = {}
        if openai_tools:
            mcp_metadata["mcp_list_tools"] = openai_tools
        if tool_calls:
            mcp_metadata["mcp_tool_calls"] = tool_calls
        if tool_results:
            mcp_metadata["mcp_call_results"] = tool_results

        if mcp_metadata:
            response._hidden_params["mcp_metadata"] = mcp_metadata
        return

    if not isinstance(response, ModelResponse):
        return

    if not hasattr(response, "choices") or not response.choices:
        return

    # Add MCP metadata to all choices' messages
    for choice in response.choices:
        message = getattr(choice, "message", None)
        if message is not None:
            # Get existing provider_specific_fields or create new dict
            provider_fields = getattr(message, "provider_specific_fields", None) or {}

            # Add MCP metadata
            if openai_tools:
                provider_fields["mcp_list_tools"] = openai_tools
            if tool_calls:
                provider_fields["mcp_tool_calls"] = tool_calls
            if tool_results:
                provider_fields["mcp_call_results"] = tool_results

            # Set the provider_specific_fields
            setattr(message, "provider_specific_fields", provider_fields)

