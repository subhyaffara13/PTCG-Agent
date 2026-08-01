
def _resolve_targeted_model_ids(
    model_list: list, model: Optional[str], model_id: Optional[str]
) -> Optional[set]:
    """
    Resolve a ``/health`` ``model`` / ``model_id`` query param to the set of
    deployment IDs the response should be scoped to.

    Mirrors the live-path semantics in ``perform_health_check()``: ``model``
    matches either the deployment's ``model_name`` alias or its
    ``litellm_params.model`` provider string. ``model_id`` matches
    ``model_info.id``.

    Both query params are validated against the supplied ``model_list``.
    Callers pass an already-scoped list (filtered to the caller's allowed
    models for non-admins, full list for admins), so a ``model_id`` that
    isn't present resolves to an empty set rather than a single-element
    set — preventing a non-admin from reading another deployment's cached
    health entry by guessing its ID.

    Returns ``None`` when no targeting is requested — callers should treat
    that as "no filter."
    """
    if not model and not model_id:
        return None
    target_ids: set = set()
    for m in model_list:
        deployment_id = (m.get("model_info") or {}).get("id")
        if not deployment_id:
            continue
        if model_id and deployment_id == model_id:
            target_ids.add(deployment_id)
            continue
        if model:
            litellm_model = (m.get("litellm_params") or {}).get("model")
            if m.get("model_name") == model or litellm_model == model:
                target_ids.add(deployment_id)
    return target_ids

