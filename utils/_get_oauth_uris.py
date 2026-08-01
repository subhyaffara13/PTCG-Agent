
def _get_oauth_uris(route_prefix: str = "/") -> tuple[str, str, str]:
    route_prefix = route_prefix.strip("/")
    if route_prefix:
        route_prefix = f"/{route_prefix}"
    return (
        f"{route_prefix}/oauth/huggingface/login",
        f"{route_prefix}/oauth/huggingface/callback",
        f"{route_prefix}/oauth/huggingface/logout",
    )

