
def parse_iam_endpoint_from_url(url: str) -> IAMEndpoint:
    """Parse an IAMEndpoint from a Postgres URL.

    Used so a reader URL can drive its own IAM refresh without requiring
    callers to set parallel DATABASE_HOST_READ_REPLICA / etc. env vars.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.hostname or not parsed.username:
        raise ValueError("Cannot parse IAM endpoint from URL: missing host or username")
    name = (parsed.path or "/").lstrip("/")
    if not name:
        raise ValueError("Cannot parse IAM endpoint from URL: missing database name")
    port = str(parsed.port) if parsed.port else "5432"
    schema: str | None = None
    if parsed.query:
        qs = urllib.parse.parse_qs(parsed.query)
        schema_vals = qs.get("schema")
        if schema_vals:
            schema = schema_vals[0]
    return IAMEndpoint(
        host=parsed.hostname,
        port=port,
        user=parsed.username,
        name=name,
        schema=schema,
    )

