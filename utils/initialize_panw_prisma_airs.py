
def initialize_panw_prisma_airs(litellm_params, guardrail):
    from litellm.proxy.guardrails.guardrail_hooks.panw_prisma_airs import (
        PanwPrismaAirsHandler,
    )

    if not litellm_params.api_key:
        raise ValueError("PANW Prisma AIRS: api_key is required")
    if not litellm_params.profile_name:
        raise ValueError("PANW Prisma AIRS: profile_name is required")

    _panw_callback = PanwPrismaAirsHandler(
        guardrail_name=guardrail.get(
            "guardrail_name", "panw_prisma_airs"
        ),  # Use .get() with default
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base
        or "https://service.api.aisecurity.paloaltonetworks.com/v1/scan/sync/request",
        profile_name=litellm_params.profile_name,
        default_on=litellm_params.default_on,
        mask_on_block=getattr(litellm_params, "mask_on_block", False),
        mask_request_content=getattr(litellm_params, "mask_request_content", False),
        mask_response_content=getattr(litellm_params, "mask_response_content", False),
        app_name=getattr(litellm_params, "app_name", None),
        fallback_on_error=getattr(litellm_params, "fallback_on_error", "block"),
        # `timeout` is now declared on BaseLitellmParams (Optional[float] = None),
        # so the attribute always exists. The Pydantic validator on LitellmParams
        # coerces strings to float, but None still means "use handler default" —
        # guard against float(None) here.
        timeout=(
            float(getattr(litellm_params, "timeout", None))
            if getattr(litellm_params, "timeout", None) is not None
            else 10.0
        ),
        violation_message_template=litellm_params.violation_message_template,
    )
    litellm.logging_callback_manager.add_litellm_callback(_panw_callback)

    return _panw_callback

