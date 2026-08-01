
def _get_cooldown_deployments(
    litellm_router_instance: LitellmRouter, parent_otel_span: Optional[Span]
) -> List[str]:
    """
    Get the list of models being cooled down for this minute
    """
    # get the current cooldown list for that minute

    # ----------------------
    # Return cooldown models
    # ----------------------
    model_ids = litellm_router_instance.get_model_ids()

    cooldown_models = litellm_router_instance.cooldown_cache.get_active_cooldowns(
        model_ids=model_ids, parent_otel_span=parent_otel_span
    )

    cached_value_deployment_ids = []
    if (
        cooldown_models is not None
        and isinstance(cooldown_models, list)
        and len(cooldown_models) > 0
        and isinstance(cooldown_models[0], tuple)
    ):
        cached_value_deployment_ids = [cv[0] for cv in cooldown_models]

    return cached_value_deployment_ids

