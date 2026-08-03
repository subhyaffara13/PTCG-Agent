from typing import Any, Dict, Optional

def _build_merged_agent_card(
    upstream_card: Optional[Mapping[str, Any]],
    *,
    agent_id: str,
    http_request: Request,
    agent_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Apply the LiteLLM-fronting merge to ``upstream_card`` for ``agent_id``."""
    proxy_base = _proxy_base_url(http_request)
    # Prefer a card-supplied ``name`` (the discovery UI exposes an editable
    # "Name (shown to API clients)" field that flows into
    # ``agent_card_params.name``) over the internal ``agent_name`` identifier.
    # Fall back to ``agent_name`` only when the card itself has no name.
    card_name = upstream_card.get("name") if upstream_card else None
    return merge_agent_card(
        upstream_card,
        proxy_url=f"{proxy_base}/a2a/{agent_id}",
        proxy_base_url=proxy_base,
        name=card_name or agent_name,
    )

