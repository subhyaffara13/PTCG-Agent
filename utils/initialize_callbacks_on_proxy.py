
def initialize_callbacks_on_proxy(
    value: Any,
    premium_user: bool,
    config_file_path: str,
    litellm_settings: dict,
    callback_specific_params: Optional[dict] = None,
):
    if not isinstance(callback_specific_params, dict):
        callback_specific_params = {}
    from litellm.integrations.custom_logger import CustomLogger
    from litellm.litellm_core_utils.logging_callback_manager import (
        LoggingCallbackManager,
    )
    from litellm.proxy.proxy_server import prisma_client

    verbose_proxy_logger.debug(
        f"{blue_color_code}initializing callbacks={value} on proxy{reset_color_code}"
    )
    if isinstance(value, list):
        imported_list: List[Any] = []
        for callback in value:  # ["presidio", <my-custom-callback>]
            if isinstance(callback, str) and callback == "compression_interception":
                from litellm.integrations.compression_interception.handler import (
                    CompressionInterceptionLogger,
                )

                compression_interception_obj = (
                    CompressionInterceptionLogger.initialize_from_proxy_config(
                        litellm_settings=litellm_settings,
                        callback_specific_params=callback_specific_params,
                    )
                )
                imported_list.append(compression_interception_obj)
                continue

            # check if callback is a custom logger compatible callback
            if isinstance(callback, str):
                callback = LoggingCallbackManager._add_custom_callback_generic_api_str(
                    callback
                )
            if (
                isinstance(callback, str)
                and callback in litellm._known_custom_logger_compatible_callbacks
            ):
                imported_list.append(callback)
            elif isinstance(callback, str) and callback == "presidio":
                from litellm.proxy.guardrails.guardrail_hooks.presidio import (
                    _OPTIONAL_PresidioPIIMasking,
                )

                presidio_logging_only: Optional[bool] = litellm_settings.get(
                    "presidio_logging_only", None
                )
                if presidio_logging_only is not None:
                    presidio_logging_only = bool(
                        presidio_logging_only
                    )  # validate boolean given

                _presidio_params = {}
                if "presidio" in callback_specific_params and isinstance(
                    callback_specific_params["presidio"], dict
                ):
                    _presidio_params = callback_specific_params["presidio"]

                params: Dict[str, Any] = {
                    "logging_only": presidio_logging_only,
                    **_presidio_params,
                }
                pii_masking_object = _OPTIONAL_PresidioPIIMasking(**params)
                imported_list.append(pii_masking_object)
            elif isinstance(callback, str) and callback == "llamaguard_moderations":
                try:
                    from litellm_enterprise.enterprise_callbacks.llama_guard import (
                        _ENTERPRISE_LlamaGuard,
                    )
                except ImportError:
                    raise Exception(
                        "MissingTrying to use Llama Guard"
                        + CommonProxyErrors.missing_enterprise_package.value
                    )

                if premium_user is not True:
                    raise Exception(
                        "Trying to use Llama Guard"
                        + CommonProxyErrors.not_premium_user.value
                    )

                llama_guard_object = _ENTERPRISE_LlamaGuard()
                imported_list.append(llama_guard_object)
            elif isinstance(callback, str) and callback == "hide_secrets":
                try:
                    from litellm_enterprise.enterprise_callbacks.secret_detection import (
                        _ENTERPRISE_SecretDetection,
                    )
                except ImportError:
                    raise Exception(
                        "Trying to use Secret Detection"
                        + CommonProxyErrors.missing_enterprise_package.value
                    )

                if premium_user is not True:
                    raise Exception(
                        "Trying to use secret hiding"
                        + CommonProxyErrors.not_premium_user.value
                    )

                _secret_detection_object = _ENTERPRISE_SecretDetection()
                imported_list.append(_secret_detection_object)
            elif isinstance(callback, str) and callback == "openai_moderations":
                try:
                    from enterprise.enterprise_hooks.openai_moderation import (
                        _ENTERPRISE_OpenAI_Moderation,
                    )
                except ImportError:
                    raise Exception(
                        "Trying to use OpenAI Moderations Check,"
                        + CommonProxyErrors.missing_enterprise_package_docker.value
                    )

                if premium_user is not True:
                    raise Exception(
                        "Trying to use OpenAI Moderations Check"
                        + CommonProxyErrors.not_premium_user.value
                    )

                openai_moderations_object = _ENTERPRISE_OpenAI_Moderation()
                imported_list.append(openai_moderations_object)
            elif isinstance(callback, str) and callback == "lakera_prompt_injection":
                from litellm.proxy.guardrails.guardrail_hooks.lakera_ai import (
                    lakeraAI_Moderation,
                )

                init_params = {}
                if (
                    "lakera_prompt_injection" in callback_specific_params
                    and isinstance(
                        callback_specific_params["lakera_prompt_injection"], dict
                    )
                ):
                    init_params = callback_specific_params["lakera_prompt_injection"]
                lakera_moderations_object = lakeraAI_Moderation(**init_params)
                imported_list.append(lakera_moderations_object)
            elif isinstance(callback, str) and callback == "aporia_prompt_injection":
                from litellm.proxy.guardrails.guardrail_hooks.aporia_ai.aporia_ai import (
                    AporiaGuardrail,
                )

                aporia_guardrail_object = AporiaGuardrail()
                imported_list.append(aporia_guardrail_object)
            elif isinstance(callback, str) and callback == "google_text_moderation":
                try:
                    from enterprise.enterprise_hooks.google_text_moderation import (
                        _ENTERPRISE_GoogleTextModeration,
                    )
                except ImportError:
                    raise Exception(
                        "Trying to use Google Text Moderation,"
                        + CommonProxyErrors.missing_enterprise_package_docker.value
                    )

                if premium_user is not True:
                    raise Exception(
                        "Trying to use Google Text Moderation"
                        + CommonProxyErrors.not_premium_user.value
                    )

                google_text_moderation_obj = _ENTERPRISE_GoogleTextModeration()
                imported_list.append(google_text_moderation_obj)
            elif isinstance(callback, str) and callback == "llmguard_moderations":
                try:
                    from litellm_enterprise.enterprise_callbacks.llm_guard import (
                        _ENTERPRISE_LLMGuard,
                    )
                except ImportError:
                    raise Exception(
                        "Trying to use Llm Guard"
                        + CommonProxyErrors.missing_enterprise_package.value
                    )

                if premium_user is not True:
                    raise Exception(
                        "Trying to use Llm Guard"
                        + CommonProxyErrors.not_premium_user.value
                    )

                llm_guard_moderation_obj = _ENTERPRISE_LLMGuard()
                imported_list.append(llm_guard_moderation_obj)
            elif isinstance(callback, str) and callback == "blocked_user_check":
                try:
                    from enterprise.enterprise_hooks.blocked_user_list import (
                        _ENTERPRISE_BlockedUserList,
                    )
                except ImportError:
                    raise Exception(
                        "Trying to use Blocked User List"
                        + CommonProxyErrors.missing_enterprise_package_docker.value
                    )

                if premium_user is not True:
                    raise Exception(
                        "Trying to use ENTERPRISE BlockedUser"
                        + CommonProxyErrors.not_premium_user.value
                    )

                blocked_user_list = _ENTERPRISE_BlockedUserList(
                    prisma_client=prisma_client
                )
                imported_list.append(blocked_user_list)
            elif isinstance(callback, str) and callback == "banned_keywords":
                try:
                    from enterprise.enterprise_hooks.banned_keywords import (
                        _ENTERPRISE_BannedKeywords,
                    )
                except ImportError:
                    raise Exception(
                        "Trying to use Banned Keywords"
                        + CommonProxyErrors.missing_enterprise_package_docker.value
                    )

                if premium_user is not True:
                    raise Exception(
                        "Trying to use ENTERPRISE BannedKeyword"
                        + CommonProxyErrors.not_premium_user.value
                    )

                banned_keywords_obj = _ENTERPRISE_BannedKeywords()
                imported_list.append(banned_keywords_obj)
            elif isinstance(callback, str) and callback == "detect_prompt_injection":
                from litellm.proxy.hooks.prompt_injection_detection import (
                    _OPTIONAL_PromptInjectionDetection,
                )

                prompt_injection_params = None
                if "prompt_injection_params" in litellm_settings:
                    prompt_injection_params_in_config = litellm_settings[
                        "prompt_injection_params"
                    ]
                    prompt_injection_params = LiteLLMPromptInjectionParams(
                        **prompt_injection_params_in_config
                    )

                prompt_injection_detection_obj = _OPTIONAL_PromptInjectionDetection(
                    prompt_injection_params=prompt_injection_params,
                )
                imported_list.append(prompt_injection_detection_obj)
            elif isinstance(callback, str) and callback == "batch_redis_requests":
                from litellm.proxy.hooks.batch_redis_get import (
                    _PROXY_BatchRedisRequests,
                )

                batch_redis_obj = _PROXY_BatchRedisRequests()
                imported_list.append(batch_redis_obj)
            elif isinstance(callback, str) and callback == "azure_content_safety":
                from litellm.proxy.hooks.azure_content_safety import (
                    _PROXY_AzureContentSafety,
                )

                azure_content_safety_params = litellm_settings[
                    "azure_content_safety_params"
                ]
                for k, v in azure_content_safety_params.items():
                    if (
                        v is not None
                        and isinstance(v, str)
                        and v.startswith("os.environ/")
                    ):
                        azure_content_safety_params[k] = get_secret(v)

                azure_content_safety_obj = _PROXY_AzureContentSafety(
                    **azure_content_safety_params,
                )
                imported_list.append(azure_content_safety_obj)
            elif isinstance(callback, str) and callback == "websearch_interception":
                from litellm.integrations.websearch_interception.handler import (
                    WebSearchInterceptionLogger,
                )

                websearch_interception_obj = (
                    WebSearchInterceptionLogger.initialize_from_proxy_config(
                        litellm_settings=litellm_settings,
                        callback_specific_params=callback_specific_params,
                    )
                )
                imported_list.append(websearch_interception_obj)
            elif isinstance(callback, str) and callback == "datadog_cost_management":
                from litellm.integrations.datadog.datadog_cost_management import (
                    DatadogCostManagementLogger,
                )

                init_params = {}
                if (
                    "datadog_cost_management" in callback_specific_params
                    and isinstance(
                        callback_specific_params["datadog_cost_management"], dict
                    )
                ):
                    init_params = callback_specific_params["datadog_cost_management"]
                datadog_cost_management_obj = DatadogCostManagementLogger(**init_params)
                imported_list.append(datadog_cost_management_obj)
            elif isinstance(callback, CustomLogger):
                imported_list.append(callback)
            else:
                verbose_proxy_logger.debug(
                    f"{blue_color_code} attempting to import custom calback={callback} {reset_color_code}"
                )
                imported_list.append(
                    get_instance_fn(
                        value=callback,
                        config_file_path=config_file_path,
                    )
                )
        if isinstance(litellm.callbacks, list):
            litellm.callbacks.extend(imported_list)
        else:
            litellm.callbacks = imported_list  # type: ignore

        if "prometheus" in value:
            from litellm.integrations.prometheus import PrometheusLogger

            PrometheusLogger._mount_metrics_endpoint()
    else:
        litellm.callbacks = [
            get_instance_fn(
                value=value,
                config_file_path=config_file_path,
            )
        ]
    verbose_proxy_logger.debug(
        f"{blue_color_code} Initialized Callbacks - {litellm.callbacks} {reset_color_code}"
    )

