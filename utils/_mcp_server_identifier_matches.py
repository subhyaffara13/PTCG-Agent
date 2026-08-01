
def _mcp_server_identifier_matches(server: Any, identifier: str) -> bool:
    return identifier in {
        getattr(server, "server_id", None),
        getattr(server, "alias", None),
        getattr(server, "server_name", None),
        getattr(server, "name", None),
    }

