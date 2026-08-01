
def _populate_router_guardrail_list(guardrail_list: List[Guardrail]) -> None:
    """
    Populate the router's guardrail_list from initialized guardrails.

    This enables load balancing across multiple guardrail deployments
    with the same guardrail_name.
    """
    from litellm.proxy.guardrails.guardrail_registry import IN_MEMORY_GUARDRAIL_HANDLER
    from litellm.proxy.proxy_server import llm_router
    from litellm.types.router import GuardrailTypedDict

    if llm_router is None:
        verbose_proxy_logger.debug(
            "Router not initialized yet, skipping guardrail_list population"
        )
        return

    router_guardrail_list: List[GuardrailTypedDict] = []

    for guardrail in guardrail_list:
        guardrail_id = guardrail.get("guardrail_id")
        guardrail_name = guardrail.get("guardrail_name")
        litellm_params: Any = guardrail.get("litellm_params", {})

        # Get the callback instance from the registry
        callback = None
        if guardrail_id:
            callback = IN_MEMORY_GUARDRAIL_HANDLER.guardrail_id_to_custom_guardrail.get(
                guardrail_id
            )

        # Build litellm_params dict for the router
        params_dict = (
            litellm_params.model_dump()
            if hasattr(litellm_params, "model_dump")
            else dict(litellm_params)
        )

        router_guardrail: GuardrailTypedDict = GuardrailTypedDict(
            guardrail_name=guardrail_name or "",
            litellm_params={
                "guardrail": params_dict.get("guardrail", ""),
                "mode": params_dict.get("mode", ""),
                "api_key": params_dict.get("api_key"),
                "api_base": params_dict.get("api_base"),
            },
            callback=callback,
            id=guardrail_id,
        )

        router_guardrail_list.append(router_guardrail)

    llm_router.guardrail_list = router_guardrail_list
    verbose_proxy_logger.debug(
        f"Populated router guardrail_list with {len(router_guardrail_list)} guardrails"
    )

