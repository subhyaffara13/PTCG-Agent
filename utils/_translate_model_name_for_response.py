
def _translate_model_name_for_response(model: dict) -> dict:
    """For team-scoped DB rows, replace `model_name` with the public name
    in `model_info.team_public_model_name` before returning. The DB column
    and the in-memory router index keep the internal mangled name
    (`model_name_{team_id}_{uuid}`) as the routing key -- this swap is a
    presentation-layer concern. Returns a shallow copy; never mutates.

    Without this swap the internal name leaks into `/v1/model/info` and
    `/v2/model/info`, the dashboard binds its edit form to it, and a
    non-rename save round-trips the internal name back -- corrupting
    `team_public_model_name` and the team ACL (see issue #28382).
    """
    if not isinstance(model, dict):
        return model
    model_info = model.get("model_info") or {}
    if not isinstance(model_info, dict):
        return model
    team_public = model_info.get("team_public_model_name")
    team_id = model_info.get("team_id")
    if not team_public or not team_id:
        return model
    current = model.get("model_name") or ""
    if not current.startswith(f"model_name_{team_id}_"):
        return model
    return {**model, "model_name": team_public}

