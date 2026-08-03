from typing import Optional

def filter_internal_params(
    data: dict, additional_internal_params: Optional[set] = None
) -> dict:
    """
    Filter out LiteLLM internal parameters that shouldn't be sent to provider APIs.

    This removes internal/MCP-related parameters that are used by LiteLLM internally
    but should not be included in API requests to providers.

    Args:
        data: Dictionary of parameters to filter
        additional_internal_params: Optional set of additional internal parameter names to filter

    Returns:
        Filtered dictionary with internal parameters removed
    """
    if not isinstance(data, dict):
        return data

    # Known internal parameters that should never be sent to provider APIs
    internal_params = {
        "skip_mcp_handler",
        "mcp_handler_context",
        "_skip_mcp_handler",
    }

    # Add any additional internal params if provided
    if additional_internal_params:
        internal_params.update(additional_internal_params)

    # Filter out internal parameters
    return {k: v for k, v in data.items() if k not in internal_params}

