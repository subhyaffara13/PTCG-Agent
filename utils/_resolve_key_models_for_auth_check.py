from typing import List

def _resolve_key_models_for_auth_check(valid_token: UserAPIKeyAuth) -> List[str]:
    """
    Expand key model sentinels before auth checks.

    ``all-team-models`` means inherit the parent team's allowlist — same
    semantics as ``get_key_models`` in ``model_checks.py``.

    If the key has no team_id the sentinel cannot be resolved, so the original
    model list (still containing the sentinel string) is returned unchanged.
    That string won't match any real model, so access is denied rather than
    silently falling through to unrestricted access.
    """
    models = list(valid_token.models or [])
    if SpecialModelNames.all_team_models.value in models:
        if valid_token.team_id is None:
            return models
        return list(valid_token.team_models or [])
    return models

