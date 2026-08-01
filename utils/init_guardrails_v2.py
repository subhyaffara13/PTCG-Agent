
def init_guardrails_v2(
    all_guardrails: List[Dict],
    config_file_path: Optional[str] = None,
    llm_router: Optional[Router] = None,
):
    from litellm.proxy.guardrails.guardrail_registry import IN_MEMORY_GUARDRAIL_HANDLER

    guardrail_list: List[Guardrail] = []

    for guardrail in all_guardrails:
        initialized_guardrail = IN_MEMORY_GUARDRAIL_HANDLER.initialize_guardrail(
            guardrail=cast(Guardrail, guardrail),
            config_file_path=config_file_path,
            llm_router=llm_router,
            source="config",
        )
        if initialized_guardrail:
            guardrail_list.append(initialized_guardrail)

    # verbose_proxy_logger.debug(f"\nGuardrail List:{guardrail_list}\n")

    # Populate router's guardrail_list for load balancing support
    _populate_router_guardrail_list(guardrail_list=guardrail_list)

