import os

def get_default_headers() -> dict:
    """
    Get default headers for HTTP requests.

    - Default: `User-Agent: litellm/{version}`
    - Override: set `LITELLM_USER_AGENT` to fully override the header value.
    """
    user_agent = os.environ.get("LITELLM_USER_AGENT")
    if user_agent is not None:
        return {"User-Agent": user_agent}

    return {"User-Agent": f"litellm/{version}"}


def get_default_headers() -> dict:
    """
    Get default headers for HTTP requests.

    - Default: `User-Agent: litellm/{version}`
    - Override: set `LITELLM_USER_AGENT` to fully override the header value.
    """
    user_agent = os.environ.get("LITELLM_USER_AGENT")
    if user_agent is not None:
        return {"User-Agent": user_agent}

    return {"User-Agent": f"litellm/{version}"}

