from typing import Dict, List

def _filter_models_to_user_accessible(all_models: List[Dict]) -> List[Dict]:
    """Keep only deployments the caller can use via direct access or team membership."""
    return [
        _model
        for _model in all_models
        if _model.get("model_info", {}).get("direct_access", False)
        or _model.get("model_info", {}).get("access_via_team_ids", [])
    ]

