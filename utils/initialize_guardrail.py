from typing import Any, Dict, List, Optional, Union

def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm
    from litellm.proxy.guardrails.guardrail_hooks.aim import AimGuardrail

    _aim_callback = AimGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_aim_callback)

    return _aim_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _akto_callback = AktoGuardrail(
        akto_base_url=getattr(litellm_params, "akto_base_url", None),
        akto_api_key=getattr(litellm_params, "akto_api_key", None),
        akto_account_id=getattr(litellm_params, "akto_account_id", None),
        akto_vxlan_id=getattr(litellm_params, "akto_vxlan_id", None),
        unreachable_fallback=getattr(
            litellm_params, "unreachable_fallback", "fail_closed"
        ),
        guardrail_timeout=getattr(litellm_params, "guardrail_timeout", None),
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )

    litellm.logging_callback_manager.add_litellm_callback(_akto_callback)
    return _akto_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _aporia_callback = AporiaGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_aporia_callback)

    return _aporia_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    if not litellm_params.api_key:
        raise ValueError("Azure Content Safety: api_key is required")
    if not litellm_params.api_base:
        raise ValueError("Azure Content Safety: api_base is required")

    azure_guardrail = litellm_params.guardrail.split("/")[1]

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Azure Content Safety: guardrail_name is required")

    if azure_guardrail == "prompt_shield":
        azure_content_safety_guardrail: Union[
            AzureContentSafetyPromptShieldGuardrail,
            AzureContentSafetyTextModerationGuardrail,
        ] = AzureContentSafetyPromptShieldGuardrail(
            guardrail_name=guardrail_name,
            **{
                **litellm_params.model_dump(exclude_none=True),
                "api_key": litellm_params.api_key,
                "api_base": litellm_params.api_base,
                "default_on": litellm_params.default_on,
                "event_hook": litellm_params.mode,
            },
        )
    elif azure_guardrail == "text_moderations":
        azure_content_safety_guardrail = AzureContentSafetyTextModerationGuardrail(
            guardrail_name=guardrail_name,
            **{
                **litellm_params.model_dump(exclude_none=True),
                "api_key": litellm_params.api_key,
                "api_base": litellm_params.api_base,
                "default_on": litellm_params.default_on,
                "event_hook": litellm_params.mode,
            },
        )
    else:
        raise ValueError(
            f"Azure Content Safety: {azure_guardrail} is not a valid guardrail"
        )

    litellm.logging_callback_manager.add_litellm_callback(
        azure_content_safety_guardrail
    )
    return azure_content_safety_guardrail


def initialize_guardrail(
    litellm_params: "LitellmParams",
    guardrail: "Guardrail",
) -> BlockCodeExecutionGuardrail:
    """Initialize the Block Code Execution guardrail from config."""
    import litellm

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Block Code Execution guardrail requires a guardrail_name")

    blocked_languages: Optional[List[str]] = cast(
        Optional[List[str]],
        _get_param(litellm_params, guardrail, "blocked_languages"),
    )
    action = cast(
        Literal["block", "mask"],
        _get_param(litellm_params, guardrail, "action", "block"),
    )
    confidence_threshold = float(
        cast(
            Union[int, float, str],
            _get_param(litellm_params, guardrail, "confidence_threshold", 0.5),
        )
    )
    detect_execution_intent = bool(
        _get_param(litellm_params, guardrail, "detect_execution_intent", True)
    )
    mode = _get_param(litellm_params, guardrail, "mode")
    event_hook = cast(
        Optional[Union[Literal["pre_call", "post_call", "during_call"], List[str]]],
        mode if mode is not None else DEFAULT_EVENT_HOOKS,
    )

    instance = BlockCodeExecutionGuardrail(
        guardrail_name=guardrail_name,
        blocked_languages=blocked_languages,
        action=action,
        confidence_threshold=confidence_threshold,
        detect_execution_intent=detect_execution_intent,
        event_hook=event_hook,
        default_on=bool(_get_param(litellm_params, guardrail, "default_on", False)),
    )
    litellm.logging_callback_manager.add_litellm_callback(instance)
    return instance


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm
    from litellm.proxy.guardrails.guardrail_hooks.cato_networks import (
        CatoNetworksGuardrail,
    )

    _cato_callback = CatoNetworksGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
        ssl_verify=getattr(litellm_params, "ssl_verify", None),
    )
    litellm.logging_callback_manager.add_litellm_callback(_cato_callback)

    return _cato_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Cisco AI Defense: guardrail_name is required")

    optional_params = getattr(litellm_params, "optional_params", None)

    _callback = CiscoAIDefenseGuardrail(
        guardrail_name=guardrail_name,
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        inspection_type=_get_optional_value(
            litellm_params, optional_params, "inspection_type"
        ),
        inspect_path=_get_optional_value(
            litellm_params, optional_params, "inspect_path"
        ),
        enabled_rules=_get_optional_value(
            litellm_params, optional_params, "enabled_rules"
        ),
        integration_profile_id=_get_optional_value(
            litellm_params, optional_params, "integration_profile_id"
        ),
        integration_profile_version=_get_optional_value(
            litellm_params, optional_params, "integration_profile_version"
        ),
        integration_tenant_id=_get_optional_value(
            litellm_params, optional_params, "integration_tenant_id"
        ),
        integration_type=_get_optional_value(
            litellm_params, optional_params, "integration_type"
        ),
        on_flagged_action=_get_optional_value(
            litellm_params, optional_params, "on_flagged_action"
        ),
        fallback_on_error=_get_optional_value(
            litellm_params, optional_params, "fallback_on_error"
        ),
        timeout=_get_optional_value(litellm_params, optional_params, "timeout"),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on or False,
    )
    litellm.logging_callback_manager.add_litellm_callback(_callback)

    # MCP post-tool-call hooks are dispatched through success callbacks.
    litellm.logging_callback_manager.add_litellm_success_callback(_callback)

    return _callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("CrowdStrike AIDR guardrail name is required")

    _crowdstrike_aidr_callback = CrowdStrikeAIDRHandler(
        guardrail_name=guardrail_name,
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        # Exclude during_call to prevent duplicate input events
        event_hook=[
            GuardrailEventHooks.pre_call.value,
            GuardrailEventHooks.post_call.value,
        ],
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_crowdstrike_aidr_callback)

    return _crowdstrike_aidr_callback


def initialize_guardrail(
    litellm_params: "LitellmParams", guardrail: "Guardrail"
) -> CustomCodeGuardrail:
    """
    Initialize a custom code guardrail.

    Args:
        litellm_params: Configuration parameters including the custom code
        guardrail: The guardrail configuration dict

    Returns:
        CustomCodeGuardrail instance
    """
    import litellm

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Custom code guardrail requires a guardrail_name")

    # Get the custom code from litellm_params
    custom_code = getattr(litellm_params, "custom_code", None)
    if not custom_code:
        raise ValueError(
            "Custom code guardrail requires 'custom_code' in litellm_params"
        )

    custom_code_guardrail = CustomCodeGuardrail(
        guardrail_name=guardrail_name,
        custom_code=custom_code,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )

    litellm.logging_callback_manager.add_litellm_callback(custom_code_guardrail)
    return custom_code_guardrail


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _dynamoai_callback = DynamoAIGuardrails(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_dynamoai_callback)

    return _dynamoai_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _enkryptai_callback = EnkryptAIGuardrails(
        guardrail_name=guardrail.get("guardrail_name", ""),
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        policy_name=litellm_params.policy_name,
        deployment_name=litellm_params.deployment_name,
        detectors=litellm_params.detectors,
        block_on_violation=litellm_params.block_on_violation,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_enkryptai_callback)

    return _enkryptai_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _generic_guardrail_api_callback = GenericGuardrailAPI(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        headers=getattr(litellm_params, "headers", None),
        additional_provider_specific_params=getattr(
            litellm_params, "additional_provider_specific_params", {}
        ),
        unreachable_fallback=getattr(
            litellm_params, "unreachable_fallback", "fail_closed"
        ),
        extra_headers=getattr(litellm_params, "extra_headers", None),
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )

    litellm.logging_callback_manager.add_litellm_callback(
        _generic_guardrail_api_callback
    )
    return _generic_guardrail_api_callback


def initialize_guardrail(
    litellm_params: "LitellmParams", guardrail: "Guardrail"
) -> GraySwanGuardrail:
    import litellm

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Gray Swan guardrail requires a guardrail_name")

    optional_params = getattr(litellm_params, "optional_params", None)

    grayswan_guardrail = GraySwanGuardrail(
        guardrail_name=guardrail_name,
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        on_flagged_action=_get_config_value(
            litellm_params, optional_params, "on_flagged_action"
        ),
        violation_threshold=_get_config_value(
            litellm_params, optional_params, "violation_threshold"
        ),
        reasoning_mode=_get_config_value(
            litellm_params, optional_params, "reasoning_mode"
        ),
        categories=_get_config_value(litellm_params, optional_params, "categories"),
        policy_id=_get_config_value(litellm_params, optional_params, "policy_id"),
        streaming_end_of_stream_only=_get_config_value(
            litellm_params, optional_params, "streaming_end_of_stream_only"
        )
        or False,
        streaming_sampling_rate=_get_config_value(
            litellm_params, optional_params, "streaming_sampling_rate"
        )
        or 5,
        fail_open=_get_config_value(litellm_params, optional_params, "fail_open"),
        guardrail_timeout=_get_config_value(
            litellm_params, optional_params, "guardrail_timeout"
        ),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )

    litellm.logging_callback_manager.add_litellm_callback(grayswan_guardrail)
    return grayswan_guardrail


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    if litellm_params.guard_name is None:
        raise Exception(
            "GuardrailsAIException - Please pass the Guardrails AI guard name via 'litellm_params::guard_name'"
        )

    _guardrails_ai_callback = GuardrailsAI(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
        guard_name=litellm_params.guard_name,
        guardrails_ai_api_input_format=getattr(
            litellm_params, "guardrails_ai_api_input_format", "llmOutput"
        ),
    )
    litellm.logging_callback_manager.add_litellm_callback(_guardrails_ai_callback)

    return _guardrails_ai_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    api_id = litellm_params.api_id if hasattr(litellm_params, "api_id") else None
    auth_url = litellm_params.auth_url if hasattr(litellm_params, "auth_url") else None
    version: int | None = (
        litellm_params.version if hasattr(litellm_params, "version") else None
    )

    _hiddenlayer_callback: HiddenlayerGuardrail | HiddenlayerGuardrailV2
    if not version or version < 2:
        _hiddenlayer_callback = HiddenlayerGuardrail(
            api_base=litellm_params.api_base,
            api_id=api_id,
            api_key=litellm_params.api_key,
            auth_url=auth_url,
            guardrail_name=guardrail.get("guardrail_name", ""),
            event_hook=litellm_params.mode,
            default_on=litellm_params.default_on,
        )
    else:
        _hiddenlayer_callback = HiddenlayerGuardrailV2(
            api_base=litellm_params.api_base,
            api_id=api_id,
            api_key=litellm_params.api_key,
            auth_url=auth_url,
            guardrail_name=guardrail.get("guardrail_name", ""),
            event_hook=litellm_params.mode,
            default_on=litellm_params.default_on,
        )

    litellm.logging_callback_manager.add_litellm_callback(_hiddenlayer_callback)
    return _hiddenlayer_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    if not litellm_params.auth_token:
        raise ValueError("IBM Guardrails: auth_token is required")
    if not litellm_params.base_url:
        raise ValueError("IBM Guardrails: base_url is required")
    if not litellm_params.detector_id:
        raise ValueError("IBM Guardrails: detector_id is required")

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("IBM Guardrails: guardrail_name is required")

    verify_ssl = getattr(litellm_params, "verify_ssl", True)

    # Get optional params
    optional_params = getattr(
        litellm_params, "optional_params", IBMDetectorOptionalParams()
    )
    detector_params = getattr(optional_params, "detector_params", {})
    extra_headers = getattr(optional_params, "extra_headers", {})
    score_threshold = getattr(optional_params, "score_threshold", None)
    block_on_detection = getattr(optional_params, "block_on_detection", True)

    is_detector_server = litellm_params.is_detector_server
    if is_detector_server is None:
        is_detector_server = True

    ibm_guardrail = IBMGuardrailDetector(
        guardrail_name=guardrail_name,
        auth_token=litellm_params.auth_token,
        base_url=litellm_params.base_url,
        detector_id=litellm_params.detector_id,
        is_detector_server=is_detector_server,
        detector_params=detector_params,
        extra_headers=extra_headers,
        score_threshold=score_threshold,
        block_on_detection=block_on_detection,
        verify_ssl=verify_ssl,
        default_on=litellm_params.default_on,
        event_hook=litellm_params.mode,
    )

    litellm.logging_callback_manager.add_litellm_callback(ibm_guardrail)
    return ibm_guardrail


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    if litellm_params.guard_name is None:
        raise Exception(
            "JavelinGuardrailException - Please pass the Javelin guard name via 'litellm_params::guard_name'"
        )

    _javelin_callback = JavelinGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        javelin_guard_name=litellm_params.guard_name,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on or False,
        api_version=litellm_params.api_version or "v1",
        config=litellm_params.config,
        metadata=litellm_params.metadata,
        application=litellm_params.application,
    )
    litellm.logging_callback_manager.add_litellm_callback(_javelin_callback)

    return _javelin_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _lasso_callback = LassoGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        user_id=litellm_params.lasso_user_id,
        conversation_id=litellm_params.lasso_conversation_id,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_lasso_callback)

    return _lasso_callback


def initialize_guardrail(
    litellm_params: "LitellmParams",
    guardrail: "Guardrail",
    llm_router: Optional["Router"] = None,
):
    """
    Initialize the Content Filter Guardrail.

    Args:
        litellm_params: Guardrail configuration parameters
        guardrail: Guardrail metadata

    Returns:
        Initialized ContentFilterGuardrail instance
    """
    guardrail_name = guardrail.get("guardrail_name")

    if not guardrail_name:
        raise ValueError("Content Filter: guardrail_name is required")

    content_filter_guardrail = ContentFilterGuardrail(
        guardrail_name=guardrail_name,
        guardrail_id=guardrail.get("guardrail_id"),
        policy_template=guardrail.get("policy_template"),
        patterns=litellm_params.patterns,
        blocked_words=litellm_params.blocked_words,
        blocked_words_file=litellm_params.blocked_words_file,
        event_hook=litellm_params.mode,  # type: ignore
        default_on=litellm_params.default_on or False,
        categories=getattr(litellm_params, "categories", None),
        severity_threshold=getattr(litellm_params, "severity_threshold", "medium"),
        llm_router=llm_router,
        image_model=getattr(litellm_params, "image_model", None),
        competitor_intent_config=getattr(
            litellm_params, "competitor_intent_config", None
        ),
        end_session_after_n_fails=getattr(
            litellm_params, "end_session_after_n_fails", None
        ),
        on_violation=getattr(litellm_params, "on_violation", None),
        realtime_violation_message=getattr(
            litellm_params, "realtime_violation_message", None
        ),
    )

    litellm.logging_callback_manager.add_litellm_callback(content_filter_guardrail)

    return content_filter_guardrail


def initialize_guardrail(
    litellm_params: "LitellmParams",
    guardrail: "Guardrail",
) -> LLMAsAJudgeGuardrail:
    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("llm_as_a_judge guardrail requires a guardrail_name")

    judge_model = _get_litellm_param(litellm_params, guardrail, "judge_model")
    if not judge_model:
        raise ValueError(
            "llm_as_a_judge guardrail requires judge_model in litellm_params"
        )

    criteria = _get_litellm_param(litellm_params, guardrail, "criteria") or []
    if not criteria:
        raise ValueError("llm_as_a_judge guardrail requires at least one criterion")

    weight_total = sum(float(c.get("weight", 0)) for c in criteria)
    if abs(weight_total - 100) > 0.5:
        raise ValueError(
            f"llm_as_a_judge criterion weights must sum to 100 (got {weight_total})"
        )

    on_failure = _get_litellm_param(litellm_params, guardrail, "on_failure", "block")
    if on_failure not in _VALID_ON_FAILURE:
        raise ValueError(
            f"llm_as_a_judge on_failure must be 'block' or 'log', got '{on_failure}'"
        )

    overall_threshold = float(
        _get_litellm_param(litellm_params, guardrail, "overall_threshold", 80.0)
    )

    mode = _get_litellm_param(litellm_params, guardrail, "mode")
    event_hook: Optional[GuardrailEventHooks] = None
    if isinstance(mode, str) and mode in {e.value for e in GuardrailEventHooks}:
        event_hook = GuardrailEventHooks(mode)

    instance = LLMAsAJudgeGuardrail(
        guardrail_name=guardrail_name,
        judge_model=judge_model,
        criteria=criteria,
        overall_threshold=overall_threshold,
        on_failure=on_failure,
        event_hook=event_hook,
        default_on=bool(
            _get_litellm_param(litellm_params, guardrail, "default_on", False)
        ),
    )
    litellm.logging_callback_manager.add_litellm_callback(instance)
    return instance


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    # Default to always-on. Only disable if the user explicitly sets default_on: false.
    # We check the raw guardrail dict because LitellmParams normalizes None → False,
    # making it impossible to distinguish "not set" from "explicitly false" via litellm_params.
    _raw_default_on = (
        cast(Dict[str, Any], guardrail).get("litellm_params", {}).get("default_on")
    )
    _default_on = False if _raw_default_on is False else True

    _callback = MCPEndUserPermissionGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=_default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_callback)
    return _callback


def initialize_guardrail(
    litellm_params: "LitellmParams", guardrail: "Guardrail"
) -> MCPJWTSigner:
    import litellm

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("MCPJWTSigner guardrail requires a guardrail_name")

    mode = litellm_params.mode
    if mode != "pre_mcp_call":
        raise ValueError(
            f"MCPJWTSigner guardrail '{guardrail_name}' has mode='{mode}' but must use "
            "mode='pre_mcp_call'. JWT injection only fires for MCP tool calls."
        )

    optional_params = getattr(litellm_params, "optional_params", None)

    def _get(key):  # type: ignore[no-untyped-def]
        if optional_params is not None:
            v = getattr(optional_params, key, None)
            if v is not None:
                return v
        return getattr(litellm_params, key, None)

    signer = MCPJWTSigner(
        guardrail_name=guardrail_name,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
        # Core signing
        issuer=_get("issuer"),
        audience=_get("audience"),
        ttl_seconds=_get("ttl_seconds"),
        # FR-5: verify + re-sign
        access_token_discovery_uri=_get("access_token_discovery_uri"),
        token_introspection_endpoint=_get("token_introspection_endpoint"),
        verify_issuer=_get("verify_issuer"),
        verify_audience=_get("verify_audience"),
        # FR-12: end-user identity mapping
        end_user_claim_sources=_get("end_user_claim_sources"),
        # FR-13: claim operations
        add_claims=_get("add_claims"),
        set_claims=_get("set_claims"),
        remove_claims=_get("remove_claims"),
        # FR-14: two-token model
        channel_token_audience=_get("channel_token_audience"),
        channel_token_ttl=_get("channel_token_ttl"),
        # FR-15: incoming claim validation
        required_claims=_get("required_claims"),
        optional_claims=_get("optional_claims"),
        # FR-9: debug headers
        debug_headers=_get("debug_headers") or False,
        # FR-10: configurable scopes
        allowed_scopes=_get("allowed_scopes"),
    )
    litellm.logging_callback_manager.add_litellm_callback(signer)
    return signer


def initialize_guardrail(
    litellm_params: "LitellmParams",
    guardrail: "Guardrail",
    llm_router: Optional["Router"] = None,
):
    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("MCP Security: guardrail_name is required")

    on_violation: Literal["block", "alert"] = cast(
        Literal["block", "alert"],
        getattr(litellm_params, "on_violation", "block"),
    )

    mcp_security_guardrail = MCPSecurityGuardrail(
        guardrail_name=guardrail_name,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on or False,
        on_violation=on_violation,
    )

    litellm.logging_callback_manager.add_litellm_callback(mcp_security_guardrail)
    return mcp_security_guardrail


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    tenant_id = getattr(litellm_params, "tenant_id", None)
    client_id = getattr(litellm_params, "client_id", None)

    # client_secret can be passed via the standard api_key field or as
    # a dedicated client_secret parameter.
    client_secret = litellm_params.api_key or getattr(
        litellm_params, "client_secret", None
    )

    if not tenant_id:
        raise ValueError("Microsoft Purview: tenant_id is required")
    if not client_id:
        raise ValueError("Microsoft Purview: client_id is required")
    if not client_secret:
        raise ValueError("Microsoft Purview: client_secret (or api_key) is required")

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Microsoft Purview: guardrail_name is required")

    purview_guardrail = MicrosoftPurviewDLPGuardrail(
        guardrail_name=guardrail_name,
        tenant_id=str(tenant_id),
        client_id=str(client_id),
        client_secret=str(client_secret),
        purview_app_name=str(
            getattr(litellm_params, "purview_app_name", None) or "LiteLLM"
        ),
        user_id_field=str(getattr(litellm_params, "user_id_field", None) or "user_id"),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )

    litellm.logging_callback_manager.add_litellm_callback(purview_guardrail)
    return purview_guardrail


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm
    from litellm.proxy.guardrails.guardrail_hooks.model_armor import (
        ModelArmorGuardrail,
    )

    _model_armor_callback = ModelArmorGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        template_id=litellm_params.template_id,
        project_id=litellm_params.project_id,
        location=litellm_params.location,
        credentials=litellm_params.credentials,
        api_endpoint=litellm_params.api_endpoint,
        default_on=litellm_params.default_on,
        mask_request_content=litellm_params.mask_request_content,
        mask_response_content=litellm_params.mask_response_content,
        fail_on_error=litellm_params.fail_on_error,
    )
    litellm.logging_callback_manager.add_litellm_callback(_model_armor_callback)

    return _model_armor_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    use_v2 = getattr(litellm_params, "use_v2", False)
    if isinstance(use_v2, str):
        use_v2 = use_v2.lower() == "true"
    if use_v2:
        return initialize_guardrail_v2(
            litellm_params=litellm_params, guardrail=guardrail
        )

    import litellm

    _noma_callback = NomaGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        application_id=litellm_params.application_id,
        monitor_mode=litellm_params.monitor_mode,
        block_failures=litellm_params.block_failures,
        anonymize_input=litellm_params.anonymize_input,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_noma_callback)

    return _noma_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _onyx_callback = OnyxGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_onyx_callback)

    return _onyx_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("OpenAI Moderation: guardrail_name is required")

    optional_params = getattr(litellm_params, "optional_params", None)

    openai_moderation_guardrail = OpenAIModerationGuardrail(
        guardrail_name=guardrail_name,
        **{
            **litellm_params.model_dump(exclude_none=True),
            "api_key": litellm_params.api_key,
            "api_base": litellm_params.api_base,
            "default_on": litellm_params.default_on,
            "event_hook": litellm_params.mode,
            "model": litellm_params.model,
            "streaming_end_of_stream_only": _get_config_value(
                litellm_params, optional_params, "streaming_end_of_stream_only"
            ),
            "streaming_sampling_rate": _get_config_value(
                litellm_params, optional_params, "streaming_sampling_rate"
            ),
        },
    )

    litellm.logging_callback_manager.add_litellm_callback(openai_moderation_guardrail)

    return openai_moderation_guardrail


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    """Create and register an Ovalix guardrail callback from proxy config."""
    import litellm

    tracker_api_base = getattr(litellm_params, "tracker_api_base", None)
    tracker_api_key = getattr(litellm_params, "tracker_api_key", None)
    application_id = getattr(litellm_params, "application_id", None)
    pre_checkpoint_id = getattr(litellm_params, "pre_checkpoint_id", None)
    post_checkpoint_id = getattr(litellm_params, "post_checkpoint_id", None)

    _ovalix_callback = OvalixGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        tracker_api_base=tracker_api_base,
        tracker_api_key=tracker_api_key,
        application_id=application_id,
        pre_checkpoint_id=pre_checkpoint_id,
        post_checkpoint_id=post_checkpoint_id,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_ovalix_callback)

    return _ovalix_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Pangea guardrail name is required")

    _pangea_callback = PangeaHandler(
        guardrail_name=guardrail_name,
        pangea_input_recipe=litellm_params.pangea_input_recipe,
        pangea_output_recipe=litellm_params.pangea_output_recipe,
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_pangea_callback)

    return _pangea_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    guardrail_name = guardrail.get("guardrail_name")

    # Note: api_key and profile_name can be None - handler will use env vars or API key's linked profile
    if not guardrail_name:
        raise ValueError("PANW Prisma AIRS: guardrail_name is required")

    _panw_callback = PanwPrismaAirsHandler(
        **{
            **litellm_params.model_dump(exclude_unset=True),
            "guardrail_name": guardrail_name,
            "event_hook": litellm_params.mode,
            "default_on": litellm_params.default_on or False,
        }
    )
    litellm.logging_callback_manager.add_litellm_callback(_panw_callback)

    return _panw_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("Pillar guardrail name is required")

    optional_params = getattr(litellm_params, "optional_params", None)

    _pillar_callback = PillarGuardrail(
        guardrail_name=guardrail_name,
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        on_flagged_action=getattr(litellm_params, "on_flagged_action", "monitor"),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
        async_mode=_get_config_value(litellm_params, optional_params, "async_mode"),
        persist_session=_get_config_value(
            litellm_params, optional_params, "persist_session"
        ),
        include_scanners=_get_config_value(
            litellm_params, optional_params, "include_scanners"
        ),
        include_evidence=_get_config_value(
            litellm_params, optional_params, "include_evidence"
        ),
        fallback_on_error=_get_config_value(
            litellm_params, optional_params, "fallback_on_error"
        ),
        timeout=_get_config_value(litellm_params, optional_params, "timeout"),
    )
    litellm.logging_callback_manager.add_litellm_callback(_pillar_callback)

    return _pillar_callback


def initialize_guardrail(
    litellm_params: "LitellmParams",
    guardrail: "Guardrail",
):
    import litellm

    _cb = PromptGuardGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        block_on_error=litellm_params.block_on_error,
        guardrail_name=guardrail.get(
            "guardrail_name",
            "",
        ),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(
        _cb,
    )

    return _cb


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm
    from litellm.proxy.guardrails.guardrail_hooks.prompt_security import (
        PromptSecurityGuardrail,
    )

    _prompt_security_callback = PromptSecurityGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_prompt_security_callback)

    return _prompt_security_callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _instance = QostodianNexus(
        api_base=litellm_params.api_base,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
        additional_provider_specific_params=litellm_params.additional_provider_specific_params,
        extra_headers=getattr(litellm_params, "extra_headers", None),
    )

    litellm.logging_callback_manager.add_litellm_callback(_instance)

    return _instance


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _qualifire_callback = QualifireGuardrail(
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        evaluation_id=getattr(litellm_params, "evaluation_id", None),
        prompt_injections=getattr(litellm_params, "prompt_injections", None),
        hallucinations_check=getattr(litellm_params, "hallucinations_check", None),
        grounding_check=getattr(litellm_params, "grounding_check", None),
        pii_check=getattr(litellm_params, "pii_check", None),
        content_moderation_check=getattr(
            litellm_params, "content_moderation_check", None
        ),
        tool_selection_quality_check=getattr(
            litellm_params, "tool_selection_quality_check", None
        ),
        assertions=getattr(litellm_params, "assertions", None),
        on_flagged=getattr(litellm_params, "on_flagged", "block"),
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )

    litellm.logging_callback_manager.add_litellm_callback(_qualifire_callback)

    return _qualifire_callback


def initialize_guardrail(
    litellm_params: "LitellmParams", guardrail: "Guardrail"
) -> RepelloAIGuardrail:
    import litellm

    _repelloai_callback = RepelloAIGuardrail(
        guardrail_name=guardrail["guardrail_name"],
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        asset_id=litellm_params.asset_id,
        unreachable_fallback=litellm_params.unreachable_fallback,
        event_hook=_event_hook_from_mode(litellm_params.mode),
        default_on=litellm_params.default_on or False,
    )
    litellm.logging_callback_manager.add_litellm_callback(_repelloai_callback)

    return _repelloai_callback


def initialize_guardrail(
    litellm_params: "LitellmParams", guardrail: "Guardrail"
) -> RubrikLogger:
    import litellm

    rubrik_callback = RubrikLogger(
        api_key=litellm_params.api_key,
        api_base=litellm_params.api_base,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )

    litellm.logging_callback_manager.add_litellm_callback(rubrik_callback)
    return rubrik_callback


def initialize_guardrail(
    litellm_params: "LitellmParams",
    guardrail: "Guardrail",
    llm_router: Optional["Router"] = None,
):
    """
    Initialize the Semantic Guard guardrail.

    Args:
        litellm_params: Guardrail configuration parameters
        guardrail: Guardrail metadata
        llm_router: LiteLLM Router instance (required for embeddings)

    Returns:
        Initialized SemanticGuardrail instance
    """
    guardrail_name = guardrail.get("guardrail_name")
    if not guardrail_name:
        raise ValueError("SemanticGuard: guardrail_name is required")

    if llm_router is None:
        raise ValueError(
            "SemanticGuard requires llm_router for embeddings. "
            "Configure a model_list with an embedding model."
        )

    semantic_guardrail = SemanticGuardrail(
        guardrail_name=guardrail_name,
        llm_router=llm_router,
        embedding_model=getattr(litellm_params, "embedding_model", None)
        or DEFAULT_SEMANTIC_GUARD_EMBEDDING_MODEL,
        similarity_threshold=getattr(litellm_params, "similarity_threshold", None)
        or DEFAULT_SEMANTIC_GUARD_SIMILARITY_THRESHOLD,
        route_templates=getattr(litellm_params, "route_templates", None),
        custom_routes_file=getattr(litellm_params, "custom_routes_file", None),
        custom_routes=getattr(litellm_params, "custom_routes", None),
        on_flagged_action=getattr(litellm_params, "on_flagged_action", "block"),
        event_hook=litellm_params.mode,  # type: ignore
        default_on=litellm_params.default_on or False,
    )

    litellm.logging_callback_manager.add_litellm_callback(semantic_guardrail)

    return semantic_guardrail


def initialize_guardrail(litellm_params: LitellmParams, guardrail: Guardrail):
    from litellm.proxy.guardrails.guardrail_hooks.tool_policy.tool_policy_guardrail import (
        ToolPolicyGuardrail,
    )

    _callback = ToolPolicyGuardrail(
        guardrail_name=guardrail.get("guardrail_name", "tool_policy"),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_callback)
    return _callback


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _vigil_guard_callback = VigilGuardGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        unreachable_fallback=litellm_params.unreachable_fallback,
        timeout=litellm_params.timeout,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_vigil_guard_callback)
    return _vigil_guard_callback


def initialize_guardrail(
    litellm_params: "LitellmParams",
    guardrail: "Guardrail",
):
    import litellm

    _cb = XecGuardGuardrail(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        xecguard_model=litellm_params.xecguard_model,
        policy_names=litellm_params.policy_names,
        block_on_error=litellm_params.block_on_error,
        grounding_strictness=litellm_params.grounding_strictness,
        guardrail_name=guardrail.get(
            "guardrail_name",
            "",
        ),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(
        _cb,
    )

    return _cb


def initialize_guardrail(litellm_params: "LitellmParams", guardrail: "Guardrail"):
    import litellm

    _zscaler_ai_guard_callback = ZscalerAIGuard(
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
        policy_id=litellm_params.policy_id,
        send_user_api_key_alias=litellm_params.send_user_api_key_alias,
        send_user_api_key_user_id=litellm_params.send_user_api_key_user_id,
        send_user_api_key_team_id=litellm_params.send_user_api_key_team_id,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        default_on=litellm_params.default_on,
    )
    litellm.logging_callback_manager.add_litellm_callback(_zscaler_ai_guard_callback)

    return _zscaler_ai_guard_callback

