
def initialize_guardrail_v2(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _noma_v2_callback = NomaV2Guardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        application_id=litellm_params.application_id,
        monitor_mode=litellm_params.monitor_mode,
        block_failures=litellm_params.block_failures,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_noma_v2_callback)

    return _noma_v2_callback

