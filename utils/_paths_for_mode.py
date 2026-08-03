from typing import Any, Dict, Optional, Tuple

def _paths_for_mode(
    mode: DiscoveryMode, params: Optional[Dict[str, Any]]
) -> Tuple[str, ...]:
    if mode == DiscoveryMode.WELL_KNOWN_FALLBACK:
        return AGENT_CARD_WELL_KNOWN_PATHS
    if mode == DiscoveryMode.LANGGRAPH_PLATFORM:
        return _build_langgraph_platform_paths(params)
    raise AgentCardDiscoveryError(f"unsupported discovery_mode: {mode}")

