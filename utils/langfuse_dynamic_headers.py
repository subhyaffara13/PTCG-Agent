
def langfuse_dynamic_headers(params: StandardCallbackDynamicParams) -> dict[str, str]:
    """Per-request Langfuse OTLP headers from team/key dynamic params."""
    public_key = params.get("langfuse_public_key")
    secret_key = params.get("langfuse_secret_key")
    if public_key and secret_key:
        return {
            "Authorization": _V1Langfuse._get_langfuse_authorization_header(
                public_key=public_key, secret_key=secret_key
            )
        }
    return {}

