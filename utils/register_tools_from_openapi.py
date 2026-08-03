from typing import Any, Dict

def register_tools_from_openapi(spec: Dict[str, Any], base_url: str):
    """Register MCP tools from OpenAPI specification."""
    paths = spec.get("paths", {})
    used_names: set = set()

    for path, path_item in paths.items():
        for method in ["get", "post", "put", "delete", "patch"]:
            if method in path_item:
                operation = path_item[method]

                # Generate tool name. Sanitize to ^[a-zA-Z0-9_-]+$ (lowercase)
                # so the resulting name is valid across OpenAI/Anthropic/Bedrock.
                # Many specs (e.g. GitHub REST) use tag-namespaced operationIds
                # like "actions/download-job-logs-for-workflow-run" which
                # contain '/' and would 400 at the LLM provider boundary.
                operation_id = operation.get("operationId", f"{method}_{path}")
                tool_name = sanitize_openapi_tool_name(operation_id)

                # Disambiguate collisions: two operationIds that differ only
                # by sanitized characters (e.g. "foo/list" and "foo.list")
                # would both become "foo_list". Append _2, _3, … to keep
                # every tool reachable, mirroring the Anthropic-side logic
                # in _build_anthropic_tool_name_maps.
                unique = tool_name
                n = 1
                while unique in used_names:
                    n += 1
                    suffix = f"_{n}"
                    unique = (
                        tool_name[: _OPENAPI_TOOL_NAME_MAX_LEN - len(suffix)] + suffix
                    )
                tool_name = unique
                used_names.add(tool_name)

                # Get description
                description = operation.get(
                    "summary", operation.get("description", f"{method.upper()} {path}")
                )

                # Build input schema
                input_schema = build_input_schema(operation)

                # Create tool function
                tool_func = create_tool_function(path, method, operation, base_url)
                tool_func.__name__ = tool_name
                tool_func.__doc__ = description

                # Register tool with local registry
                global_mcp_tool_registry.register_tool(
                    name=tool_name,
                    description=description,
                    input_schema=input_schema,
                    handler=tool_func,
                )
                verbose_logger.debug(f"Registered tool: {tool_name}")

