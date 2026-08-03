from typing import Dict, Optional

def _filter_reserved_headers(
    agent_extra_headers: Optional[Mapping[str, str]],
) -> Optional[Dict[str, str]]:
    """
    Strip reserved AWS / AgentCore headers from caller-supplied
    ``agent_extra_headers`` before they are merged into the signed request.

    Returns ``None`` if the result is empty.
    """
    if not agent_extra_headers:
        return None

    filtered: Dict[str, str] = {}
    dropped: list = []
    for k, v in agent_extra_headers.items():
        k_lower = k.lower()
        if k_lower in _RESERVED_EXACT_HEADERS or any(
            k_lower.startswith(prefix) for prefix in _RESERVED_PREFIX_HEADERS
        ):
            dropped.append(k)
            continue
        filtered[k] = v

    if dropped:
        verbose_logger.warning(
            "BedrockAgentCore A2A: dropping reserved header(s) from "
            "agent_extra_headers (not forwarded to AgentCore): %s",
            sorted(dropped),
        )

    return filtered or None

