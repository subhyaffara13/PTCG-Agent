from typing import Any, Dict

def build_input_schema(operation: Dict[str, Any]) -> Dict[str, Any]:
    """Build MCP input schema from OpenAPI operation."""
    properties = {}
    required = []

    # Process parameters
    if "parameters" in operation:
        for param in operation["parameters"]:
            if "name" not in param:
                continue
            param_name = param["name"]
            param_schema = param.get("schema", {})
            param_type = param_schema.get("type", "string")

            properties[param_name] = {
                "type": param_type,
                "description": param.get("description", ""),
            }

            if param.get("required", False):
                required.append(param_name)

    # Process requestBody (OpenAPI 3.x)
    if "requestBody" in operation:
        request_body = operation["requestBody"]
        content = request_body.get("content", {})

        # Try to get JSON schema
        if "application/json" in content:
            schema = content["application/json"].get("schema", {})
            properties["body"] = {
                "type": "object",
                "description": request_body.get("description", "Request body"),
                "properties": schema.get("properties", {}),
            }
            if request_body.get("required", False):
                required.append("body")

    return {
        "type": "object",
        "properties": properties,
        "required": required if required else [],
    }

