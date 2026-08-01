
def _get_validated_client_redirect_uri(
    request: Request, state_data: Dict[str, Any]
) -> str:
    """Return a trusted (same-origin, loopback, or ops-allowlisted)
    client redirect URI from OAuth state.
    """
    redirect_uri = state_data.get("client_redirect_uri") or state_data.get("base_url")
    if not redirect_uri or not isinstance(redirect_uri, str):
        raise HTTPException(status_code=400, detail="Invalid redirect URI")
    validate_trusted_redirect_uri(request, redirect_uri)
    return redirect_uri

