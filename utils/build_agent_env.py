
def build_agent_env(
    base_env: Mapping[str, str],
    base_url: str,
    api_key: str,
    profiles: FrozenSet[str],
) -> Dict[str, str]:
    """Return a copy of base_env wired to route the agent through the proxy.

    Anthropic clients (Claude Code) append /v1/messages to ANTHROPIC_BASE_URL,
    so it stays the bare proxy root; OpenAI clients (Codex, OpenCode) expect the
    /v1 suffix on OPENAI_BASE_URL. ANTHROPIC_API_KEY is dropped so a stray
    Anthropic key cannot win over the bearer token we set.
    """
    env = dict(base_env)
    root = base_url.rstrip("/")
    if PROFILE_ANTHROPIC in profiles:
        env[ANTHROPIC_BASE_URL_ENV] = root
        env[ANTHROPIC_AUTH_TOKEN_ENV] = api_key
        env.pop(ANTHROPIC_API_KEY_ENV, None)
    if PROFILE_OPENAI in profiles:
        env[OPENAI_BASE_URL_ENV] = root + "/v1"
        env[OPENAI_API_KEY_ENV] = api_key
    return env

