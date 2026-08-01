
def _set_tool_attributes(
    span: "Span", optional_tools: Optional[list], metadata_tools: Optional[list]
):
    """set tool attributes on span from optional_params or tool call metadata"""
    if optional_tools:
        for idx, tool in enumerate(optional_tools):
            if not isinstance(tool, dict):
                continue
            function = (
                tool.get("function") if isinstance(tool.get("function"), dict) else None
            )
            if not function:
                continue
            tool_name = function.get("name")
            if tool_name:
                safe_set_attribute(
                    span, f"{SpanAttributes.LLM_TOOLS}.{idx}.name", tool_name
                )
            tool_description = function.get("description")
            if tool_description:
                safe_set_attribute(
                    span,
                    f"{SpanAttributes.LLM_TOOLS}.{idx}.description",
                    tool_description,
                )
            params = function.get("parameters")
            if params is not None:
                safe_set_attribute(
                    span,
                    f"{SpanAttributes.LLM_TOOLS}.{idx}.parameters",
                    json.dumps(params),
                )

    if metadata_tools and isinstance(metadata_tools, list):
        for idx, tool in enumerate(metadata_tools):
            if not isinstance(tool, dict):
                continue
            tool_name = tool.get("name")
            if tool_name:
                safe_set_attribute(
                    span,
                    f"{SpanAttributes.LLM_INVOCATION_PARAMETERS}.tools.{idx}.name",
                    tool_name,
                )

            tool_description = tool.get("description")
            if tool_description:
                safe_set_attribute(
                    span,
                    f"{SpanAttributes.LLM_INVOCATION_PARAMETERS}.tools.{idx}.description",
                    tool_description,
                )

