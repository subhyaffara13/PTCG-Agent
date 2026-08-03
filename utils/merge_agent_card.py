from typing import Any, Dict, Optional

def merge_agent_card(
    upstream_card: Optional[Mapping[str, Any]],
    *,
    proxy_url: str,
    proxy_base_url: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build the LiteLLM-fronted agent card.

    Args:
        upstream_card: Card returned by the upstream agent's well-known endpoint.
            May be ``None``/empty when the upstream did not expose one.
        proxy_url: Full URL clients should hit to invoke this agent through
            the proxy, e.g. ``https://proxy.example.com/a2a/<agent_id>``.
        proxy_base_url: Root URL of the LiteLLM proxy, used as a fallback when
            we synthesize a provider record.
        name: User-supplied agent name from the LiteLLM UI. Takes precedence
            over the upstream card's ``name``.
        description: User-supplied description from the LiteLLM UI. Takes
            precedence over the upstream card's ``description``.

    Returns:
        A dict suitable for serving as the proxy's agent card. Only keys in
        the v1.0 AgentCard schema (plus ``supportedInterfaces``) are emitted.
    """
    base: Dict[str, Any] = deepcopy(dict(upstream_card)) if upstream_card else {}

    # Keep the upstream ``url`` on the stored card: the runtime A2A
    # invocation path reads it from ``agent_card_params`` to know where to
    # proxy requests. The public well-known endpoint rewrites this field
    # to the proxy URL before exposing the card to clients.

    base["protocolVersion"] = LITELLM_A2A_PROTOCOL_VERSION

    if name:
        base["name"] = name
    if description:
        base["description"] = description

    if not base.get("version"):
        base["version"] = _DEFAULT_AGENT_VERSION

    base["capabilities"] = _filter_capabilities(base.get("capabilities"))

    if not base.get("skills"):
        base["skills"] = deepcopy(_DEFAULT_SKILLS)
    if not base.get("defaultInputModes"):
        base["defaultInputModes"] = list(_DEFAULT_MODES)
    if not base.get("defaultOutputModes"):
        base["defaultOutputModes"] = list(_DEFAULT_MODES)

    if not base.get("provider"):
        base["provider"] = _default_litellm_provider(proxy_base_url)

    base["supportedInterfaces"] = [
        {
            "url": proxy_url,
            "protocolBinding": "JSONRPC",
            "protocolVersion": LITELLM_A2A_PROTOCOL_VERSION,
        }
    ]

    base["securitySchemes"] = deepcopy(LITELLM_SECURITY_SCHEMES)
    # Use the standard A2A/OpenAPI ``security`` field for requirements, not
    # the non-standard ``securityRequirements`` alias. The upstream's own
    # ``security`` selector is overwritten here because the proxy enforces its
    # own scheme regardless of what upstream required.
    base["security"] = deepcopy(LITELLM_SECURITY_REQUIREMENTS)

    return {key: value for key, value in base.items() if key in _ALLOWED_TOP_LEVEL_KEYS}

