
def initialize_lasso(
    litellm_params: LitellmParams,
    guardrail: Guardrail,
):
    from litellm.proxy.guardrails.guardrail_hooks.lasso import LassoGuardrail

    _lasso_callback = LassoGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        lasso_api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        user_id=litellm_params.lasso_user_id,
        conversation_id=litellm_params.lasso_conversation_id,
        mask=litellm_params.mask,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_lasso_callback)

    return _lasso_callback

