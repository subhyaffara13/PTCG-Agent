
def adapt_tool_definition_to_oci_standard(
    tools: List[Dict], vendor: OCIVendors
) -> List[OCIToolDefinition]:
    """Convert OpenAI-format tool definitions to OCI GENERIC format.

    Resolves ``$ref``/``$defs`` and ``anyOf`` that the OCI endpoint rejects.
    """
    new_tools = []
    for tool in tools:
        if tool["type"] != "function":
            raise OCIError(status_code=400, message="OCI only supports function tools")

        tool_function = tool.get("function")
        if not isinstance(tool_function, dict):
            raise OCIError(
                status_code=400, message="Tool `function` must be a dictionary"
            )

        raw_params = tool_function.get("parameters", {})
        resolved_params = sanitize_oci_schema(
            resolve_oci_schema_anyof(resolve_oci_schema_refs(raw_params))
        )

        new_tools.append(
            OCIToolDefinition(
                type="FUNCTION",
                name=tool_function.get("name"),
                description=tool_function.get("description", ""),
                parameters=resolved_params,
            )
        )

    return new_tools

