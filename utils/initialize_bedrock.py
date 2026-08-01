
def initialize_bedrock(litellm_params: LitellmParams, guardrail: Guardrail):
    from litellm.proxy.guardrails.guardrail_hooks.bedrock_guardrails import (
        BedrockGuardrail,
    )

    _bedrock_callback = BedrockGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        guardrailIdentifier=litellm_params.guardrailIdentifier,
        guardrailVersion=litellm_params.guardrailVersion,
        default_on=litellm_params.default_on,
        disable_exception_on_block=litellm_params.disable_exception_on_block,
        mask_request_content=litellm_params.mask_request_content,
        mask_response_content=litellm_params.mask_response_content,
        aws_region_name=litellm_params.aws_region_name,
        aws_access_key_id=litellm_params.aws_access_key_id,
        aws_secret_access_key=litellm_params.aws_secret_access_key,
        aws_session_token=litellm_params.aws_session_token,
        aws_session_name=litellm_params.aws_session_name,
        aws_profile_name=litellm_params.aws_profile_name,
        aws_role_name=litellm_params.aws_role_name,
        aws_web_identity_token=litellm_params.aws_web_identity_token,
        aws_sts_endpoint=litellm_params.aws_sts_endpoint,
        aws_bedrock_runtime_endpoint=litellm_params.aws_bedrock_runtime_endpoint,
        experimental_use_latest_role_message_only=litellm_params.experimental_use_latest_role_message_only,
    )
    litellm.logging_callback_manager.add_litellm_callback(_bedrock_callback)
    return _bedrock_callback

