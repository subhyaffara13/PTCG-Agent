
def _get_github_oidc_token(audience: str) -> str:
    """Mint an OIDC id token from the GitHub Actions runtime.

    Relies on the `ACTIONS_ID_TOKEN_REQUEST_URL` / `ACTIONS_ID_TOKEN_REQUEST_TOKEN` env vars,
    which GitHub only injects when the job declares `permissions: id-token: write`.
    """
    request_url = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL")
    request_token = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN")
    if not request_url or not request_token:
        raise OIDCError(
            "Cannot request an OIDC id token from GitHub Actions. Make sure the workflow job sets "
            "`permissions: id-token: write`. See "
            "https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect"
        )
    response = get_session().get(
        request_url,
        params={"audience": audience},
        headers={"Authorization": f"Bearer {request_token}"},
    )
    hf_raise_for_status(response)
    return response.json()["value"]

