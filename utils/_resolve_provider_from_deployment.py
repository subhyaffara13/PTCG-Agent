
def _resolve_provider_from_deployment(
    llm_router: Router,
    model_name: str,
    pre_alias_model_name: Optional[str] = None,
) -> Optional[str]:
    """
    Resolve a provider hint from the deployment's litellm_params when the
    user-facing model name has no provider prefix.

    Tries the post-alias name first (the resolved model group), then the
    pre-alias name. Returns None if no deployment is found or the deployment
    has no usable provider info.
    """
    candidates = [model_name]
    if pre_alias_model_name and pre_alias_model_name != model_name:
        candidates.append(pre_alias_model_name)

    for name in candidates:
        try:
            deployment = llm_router.get_deployment_by_model_group_name(
                model_group_name=name
            )
        except Exception:
            deployment = None
        if deployment is None:
            continue

        litellm_params = getattr(deployment, "litellm_params", None)
        if litellm_params is None:
            continue

        custom_provider = getattr(litellm_params, "custom_llm_provider", None)
        if custom_provider:
            return custom_provider

        deployment_model = getattr(litellm_params, "model", "") or ""
        if "/" in deployment_model:
            return deployment_model.split("/", 1)[0]

    return None

