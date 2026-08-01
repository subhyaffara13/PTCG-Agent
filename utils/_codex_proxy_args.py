
def _codex_proxy_args(base_url: str) -> List[str]:
    """Codex `-c` overrides that point it at the proxy.

    Codex ignores OPENAI_BASE_URL (it always dials api.openai.com), so the env
    profile alone cannot route it. It does honor a custom provider, so define one
    inline; supports_websockets=false forces the HTTP/SSE Responses transport
    because the proxy does not speak the Responses WebSocket protocol. The key is
    read from OPENAI_API_KEY, which build_agent_env already exports.
    """
    root = base_url.rstrip("/") + "/v1"
    provider = f"model_providers.{CODEX_PROXY_PROVIDER}"
    return [
        "-c",
        f'model_provider="{CODEX_PROXY_PROVIDER}"',
        "-c",
        f'{provider}.name="LiteLLM proxy"',
        "-c",
        f'{provider}.base_url="{root}"',
        "-c",
        f'{provider}.env_key="{OPENAI_API_KEY_ENV}"',
        "-c",
        f'{provider}.wire_api="responses"',
        "-c",
        f"{provider}.supports_websockets=false",
    ]

