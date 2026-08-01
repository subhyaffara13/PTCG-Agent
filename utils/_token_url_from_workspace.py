
def _token_url_from_workspace(workspace_url: str) -> str:
    """Build the workspace OIDC token endpoint from a workspace URL."""
    base = workspace_url.strip().rstrip("/")
    if base.endswith("/serving-endpoints"):
        base = base[: -len("/serving-endpoints")]
    return f"{base}/oidc/v1/token"

