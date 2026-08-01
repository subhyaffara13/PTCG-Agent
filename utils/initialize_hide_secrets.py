
def initialize_hide_secrets(litellm_params: LitellmParams, guardrail: Guardrail):
    try:
        from litellm_enterprise.enterprise_callbacks.secret_detection import (
            _ENTERPRISE_SecretDetection,
        )
    except ImportError:
        raise Exception(
            "Trying to use Secret Detection"
            + CommonProxyErrors.missing_enterprise_package.value
        )

    _secret_detection_object = _ENTERPRISE_SecretDetection(
        detect_secrets_config=litellm_params.detect_secrets_config,
        event_hook=litellm_params.mode,
        guardrail_name=guardrail.get("guardrail_name", ""),
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_secret_detection_object)
    return _secret_detection_object

