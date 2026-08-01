
def _fetch_agentops_jwt(api_key: str) -> dict[str, Any]:
    # Own a short-lived client rather than ``_get_httpx_client()``: that returns
    # a process-wide cached ``HTTPHandler`` whose connection pool is shared by
    # every caller, so closing it here would break concurrent/subsequent
    # requests. This one-shot auth call gets its own client to close.
    with httpx.Client(timeout=10) as client:
        response = client.post(
            url=_AGENTOPS_AUTH_ENDPOINT,
            headers={"Content-Type": "application/json", "Connection": "keep-alive"},
            json={"api_key": api_key},
        )
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch AgentOps token: {response.text}")
        return response.json()

