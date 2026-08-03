from typing import Callable

def verify_proxy_key(
    base_url: str,
    api_key: str,
    *,
    get: Callable[..., requests.Response] = requests.get,
) -> None:
    """Probe the proxy with the key so bad creds fail here, not inside the agent.

    Raises AgentRunError when the proxy is unreachable or rejects the key. Other
    non-2xx responses are tolerated; the agent's own call is the real test.
    """
    url = base_url.rstrip("/") + "/v1/models"
    try:
        resp = get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
    except requests.RequestException as e:
        raise AgentRunError(
            f"Could not reach the LiteLLM proxy at {base_url.rstrip('/')}: {e}. "
            "Is it running, and is --base-url (or LITELLM_PROXY_URL) correct?"
        )
    if resp.status_code in (401, 403):
        raise AgentRunError(
            f"LiteLLM rejected your key (HTTP {resp.status_code}). "
            "Run `lite login` to refresh it, or pass a valid --api-key."
        )

