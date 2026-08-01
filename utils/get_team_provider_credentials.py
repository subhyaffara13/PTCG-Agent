
def get_team_provider_credentials(
    llm_router: Optional["Router"],
    team_models: List[str],
    custom_llm_provider: str,
    team_id: Optional[str] = None,
) -> Optional[dict]:
    """
    Resolve upstream credentials for a provider-scoped file operation
    (e.g. GET /v1/files), which doesn't pin a model.

    Priority:
    1. The team's own (BYOK) deployment for this provider — a deployment whose
       ``model_info.team_id`` matches ``team_id``. This keeps team-scoped listings
       on the team's own provider account/key instead of a shared global one.
    2. Fallback: any deployment the team is granted access to for this provider,
       expanding wildcard routes and the all-proxy-models sentinel.

    Credential lookup is always scoped to the team's allowlist, so a team can
    never resolve a provider key for a deployment it isn't authorized to use.
    Returns None when the router is unavailable or no authorized deployment
    matches, so the caller can fall back to default credential resolution.
    """
    if llm_router is None:
        return None

    def _provider_credentials(model_id: str) -> Optional[dict]:
        credentials = llm_router.get_deployment_credentials_with_provider(
            model_id=model_id
        )
        if (
            credentials is not None
            and credentials.get("custom_llm_provider") == custom_llm_provider
        ):
            return credentials
        return None

    # 1. Prefer the team's own BYOK deployment, matched by model_info.team_id.
    if team_id is not None:
        for deployment in llm_router.model_list or []:
            model_info = deployment.get("model_info") or {}
            if model_info.get("team_id") != team_id:
                continue
            deployment_id = model_info.get("id")
            if deployment_id is None:
                continue
            credentials = _provider_credentials(deployment_id)
            if credentials is not None:
                return credentials

    # 2. Fall back to deployments the team is allowed to access. The
    #    all-proxy-models sentinel isn't expanded by get_complete_model_list, so
    #    normalize it to an empty allowlist, which defers to the team-scoped
    #    proxy model list. A team with a restricted allowlist (e.g. anthropic
    #    only) therefore never resolves another provider's key.
    from litellm.proxy._types import SpecialModelNames
    from litellm.proxy.auth.model_checks import get_complete_model_list

    grants_all_models = SpecialModelNames.all_proxy_models.value in team_models
    effective_team_models = [] if grants_all_models else team_models

    proxy_model_list = llm_router.get_model_names(team_id=team_id)
    model_access_groups = llm_router.get_model_access_groups()
    models_to_try = list(
        dict.fromkeys(
            get_complete_model_list(
                key_models=[],
                team_models=effective_team_models,
                proxy_model_list=proxy_model_list,
                user_model=None,
                infer_model_from_keys=False,
                return_wildcard_routes=True,
                llm_router=llm_router,
                model_access_groups=model_access_groups,
                include_model_access_groups=True,
                team_id=team_id,
            )
        )
    )
    for model_name in models_to_try:
        credentials = _provider_credentials(model_name)
        if credentials is not None:
            return credentials

    return None

