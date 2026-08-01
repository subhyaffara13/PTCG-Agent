
def _build_duckdb_secret_statements(token: str | bool | None) -> list[str]:
    if token is None or token is True:
        token = get_token()

    if not token:
        return []

    escaped_token = token.replace("'", "''")
    escaped_endpoint = constants.ENDPOINT.replace("'", "''")
    return [
        f"CREATE OR REPLACE SECRET hf_hub_token (TYPE HTTP, BEARER_TOKEN '{escaped_token}', SCOPE '{escaped_endpoint}')",
        f"CREATE OR REPLACE SECRET hf_token (TYPE HUGGINGFACE, TOKEN '{escaped_token}')",
    ]

