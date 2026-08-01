
def _warn_on_server_name_fields(
    *,
    server_id: str,
    alias: Optional[str],
    server_name: Optional[str],
):
    def _warn(field_name: str, value: Optional[str]) -> None:
        if not value:
            return
        result = validate_tool_name(value)
        if result.is_valid:
            return

        warning_text = (
            "; ".join(result.warnings) if result.warnings else "Validation failed"
        )
        verbose_logger.warning(
            "MCP server '%s' has invalid %s '%s': %s",
            server_id,
            field_name,
            value,
            warning_text,
        )

    _warn("alias", alias)
    _warn("server_name", server_name)

