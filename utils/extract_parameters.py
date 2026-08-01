
def extract_parameters(node: _ProfilerEvent) -> Iterator[TensorKey]:
    for p, _p_grad in _extract_parameters_and_gradients(node):
        if p is not None:
            yield p


def extract_parameters(operation: Dict[str, Any]) -> tuple:
    """Extract parameter names from OpenAPI operation."""
    path_params = []
    query_params = []
    body_params = []

    # OpenAPI 3.x and 2.x parameters
    if "parameters" in operation:
        for param in operation["parameters"]:
            if "name" not in param:
                continue
            param_name = param["name"]
            if param.get("in") == "path":
                path_params.append(param_name)
            elif param.get("in") == "query":
                query_params.append(param_name)
            elif param.get("in") == "body":
                body_params.append(param_name)

    # OpenAPI 3.x requestBody
    if "requestBody" in operation:
        body_params.append("body")

    return path_params, query_params, body_params

