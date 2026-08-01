
def initialize_lakera_v2(litellm_params: LitellmParams, guardrail: Guardrail):
    from litellm.proxy.guardrails.guardrail_hooks.lakera_ai_v2 import LakeraAIGuardrail

    _lakera_v2_callback = LakeraAIGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
        project_id=litellm_params.project_id,
        payload=litellm_params.payload,
        breakdown=litellm_params.breakdown,
        metadata=litellm_params.metadata,
        dev_info=litellm_params.dev_info,
        on_flagged=litellm_params.on_flagged,
    )
    litellm.logging_callback_manager.add_litellm_callback(_lakera_v2_callback)
    return _lakera_v2_callback

