
def _get_weave_authorization_header(api_key: str) -> str:
    """
    Get the authorization header for Weave OpenTelemetry.

    Weave uses Basic auth with format: api:<WANDB_API_KEY>
    """
    auth_string = f"api:{api_key}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    return f"Basic {auth_header}"

