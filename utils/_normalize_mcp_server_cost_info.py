
def _normalize_mcp_server_cost_info(mcp_info: MCPInfo) -> None:
    """Coerce ``mcp_server_cost_info`` numeric fields to ``float`` at ingest.

    YAML 1.1 parses scientific notation without a decimal point (e.g.
    ``7e-05``) as a string, and ``MCPServerCostInfo`` is a TypedDict with no
    runtime validation, so string-typed costs flow through to the UI and
    crash its ``.toFixed`` formatting. Values that cannot be coerced are
    dropped with a warning instead of failing the server load.
    """
    cost_info = mcp_info.get("mcp_server_cost_info")
    if not isinstance(cost_info, dict):
        return

    server_name = mcp_info.get("server_name")
    normalized = dict(cost_info)

    default_cost = normalized.get("default_cost_per_query")
    if default_cost is not None:
        try:
            normalized["default_cost_per_query"] = float(default_cost)
        except (TypeError, ValueError):
            verbose_logger.warning(
                "MCP server '%s' has non-numeric default_cost_per_query %r; ignoring it",
                server_name,
                default_cost,
            )
            del normalized["default_cost_per_query"]

    tool_costs = normalized.get("tool_name_to_cost_per_query")
    if isinstance(tool_costs, dict):
        normalized_tool_costs = {}
        for tool_name, cost in tool_costs.items():
            try:
                normalized_tool_costs[tool_name] = float(cost)
            except (TypeError, ValueError):
                verbose_logger.warning(
                    "MCP server '%s' has non-numeric cost %r for tool '%s'; ignoring it",
                    server_name,
                    cost,
                    tool_name,
                )
        normalized["tool_name_to_cost_per_query"] = normalized_tool_costs

    mcp_info["mcp_server_cost_info"] = normalized

