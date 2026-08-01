
def _redact_env_var_values(response: dict) -> None:
    """Blank ``env_vars[].value`` in a management response before telemetry.

    MCP endpoints return decrypted ``scope="global"`` env var values so the admin
    UI can pre-fill the edit form; those values are upstream credentials and must
    not be serialized verbatim into OTEL spans, where an observability user could
    read them. The values surface both at the top level (single-server
    create/update) and nested under ``items`` (the submissions queue), so both are
    scrubbed. Names, scopes, and descriptions are kept so traces stay useful.
    """
    if isinstance(response.get("env_vars"), list):
        response["env_vars"] = [
            _redacted_env_var(entry) for entry in response["env_vars"]
        ]

    items = response.get("items")
    if isinstance(items, list):
        response["items"] = [_redact_record_env_vars(item) for item in items]

