from typing import Any, Dict, Set

def _deployment_matches_allowed_model_names(
    model: Dict[str, Any], allowed_model_names: Set[str]
) -> bool:
    """Match a router deployment against allowed public model names.

    Team-scoped rows store an internal routing key in ``model_name``; callers
    with key/team restrictions still refer to the public name in
    ``model_info.team_public_model_name``.
    """
    if model.get("model_name") in allowed_model_names:
        return True
    model_info = model.get("model_info")
    if not isinstance(model_info, dict):
        return False
    team_public_model_name = model_info.get("team_public_model_name")
    return (
        isinstance(team_public_model_name, str)
        and team_public_model_name in allowed_model_names
    )

