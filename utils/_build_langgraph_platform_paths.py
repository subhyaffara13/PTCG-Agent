
def _build_langgraph_platform_paths(
    params: Optional[Dict[str, Any]],
) -> Tuple[str, ...]:
    """Build the paths to try for LangGraph Platform discovery.

    LangGraph serves the card at ``/.well-known/agent-card.json`` with the
    ``assistant_id`` carried as a query parameter. We still try the other
    A2A path variants (with the same query string appended) so we degrade
    gracefully if a deployment uses an older spec name.
    """
    assistant_id = (params or {}).get("assistant_id")
    if not assistant_id:
        raise AgentCardDiscoveryError(
            "langgraph_platform discovery requires params.assistant_id"
        )
    query = urlencode({"assistant_id": str(assistant_id)})
    return tuple(f"{path}?{query}" for path in AGENT_CARD_WELL_KNOWN_PATHS)

