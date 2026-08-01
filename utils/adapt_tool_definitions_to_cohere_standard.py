
def adapt_tool_definitions_to_cohere_standard(
    tools: List[Dict[str, Any]],
) -> List[CohereTool]:
    """Adapt OpenAI-format tool definitions to the OCI Cohere format.

    - Resolves ``$ref``/``$defs`` and ``anyOf`` patterns that OCI rejects.
    - Maps JSON Schema type names to Python type names (``"string"`` → ``"str"``).
    - Embeds unsupported constraints (enum, format, range, pattern) into the
      parameter description so the model can still see them.
    """
    cohere_tools = []
    for tool in tools:
        function_def = tool.get("function", {})
        raw_params = function_def.get("parameters", {})

        resolved = sanitize_oci_schema(
            resolve_oci_schema_anyof(resolve_oci_schema_refs(raw_params))
        )
        properties = resolved.get("properties", {})
        required = resolved.get("required", [])

        parameter_definitions = {}
        for param_name, param_schema in properties.items():
            json_type = param_schema.get("type", "string")
            python_type = OCI_JSON_TO_PYTHON_TYPES.get(json_type, json_type)
            parameter_definitions[param_name] = CohereParameterDefinition(
                description=enrich_cohere_param_description(
                    param_schema.get("description", ""), param_schema
                ),
                type=python_type,
                isRequired=param_name in required,
            )

        cohere_tools.append(
            CohereTool(
                name=function_def.get("name", ""),
                description=function_def.get("description", ""),
                parameterDefinitions=parameter_definitions,
            )
        )

    return cohere_tools

