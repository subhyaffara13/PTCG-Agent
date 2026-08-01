
def parse_databricks_oauth_config(
    litellm_params: Optional[Dict[str, Any]],
) -> Optional[DatabricksAppOAuthConfig]:
    """Build a Databricks App OAuth config from an agent's ``litellm_params``.

    Returns ``None`` when the agent has no ``databricks_oauth`` block. Raises
    ``ValueError`` when the block is present but incomplete, so misconfiguration
    surfaces loudly instead of silently sending an unauthenticated request.
    """
    if not litellm_params:
        return None

    raw = litellm_params.get(DATABRICKS_OAUTH_PARAM)
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError(
            f"'{DATABRICKS_OAUTH_PARAM}' must be a mapping of OAuth settings, "
            f"got {type(raw).__name__}"
        )

    client_id = _resolve_secret(raw.get("client_id"))
    client_secret = _resolve_secret(raw.get("client_secret"))
    workspace_url = _resolve_secret(raw.get("workspace_url"))

    missing = [
        name
        for name, value in (
            ("client_id", client_id),
            ("client_secret", client_secret),
            ("workspace_url", workspace_url),
        )
        if not value
    ]
    if missing:
        raise ValueError(
            f"Databricks App OAuth config is missing required field(s): "
            f"{', '.join(missing)}"
        )

    scope = _resolve_secret(raw.get("scope")) or _DEFAULT_SCOPE

    return DatabricksAppOAuthConfig(
        client_id=client_id,  # type: ignore[arg-type]
        client_secret=client_secret,  # type: ignore[arg-type]
        token_url=_token_url_from_workspace(workspace_url),  # type: ignore[arg-type]
        scope=scope,
    )

