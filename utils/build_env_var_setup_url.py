
def build_env_var_setup_url(server_id: str) -> str:
    """The frontend URL where a user can fill in their per-user env vars."""
    base = os.environ.get("PROXY_BASE_URL", "").rstrip("/")
    path = f"/ui/?page=mcp-servers&fill_env_vars={quote(server_id, safe='')}"
    return f"{base}{path}" if base else path

