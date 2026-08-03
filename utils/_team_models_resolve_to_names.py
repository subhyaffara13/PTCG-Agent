from typing import Any, Dict, List

def _team_models_resolve_to_names(
    team_models: List[str], access_groups: Dict[str, Any]
) -> List[str]:
    """Expand team model entries (including access group names) to concrete model names."""
    resolved: List[str] = []
    for name in team_models:
        if name in access_groups:
            resolved.extend(access_groups[name])
        else:
            resolved.append(name)
    return resolved

