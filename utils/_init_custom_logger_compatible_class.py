import os
from typing import Any, Optional

def _init_custom_logger_compatible_class(
    logging_integration: _custom_logger_compatible_callbacks_literal,
    internal_usage_cache: Optional[DualCache],
    llm_router: Optional[
        Any
    ],  # expect litellm.Router, but typing errors due to circular import
    custom_logger_init_args: Optional[dict] = {},
) -> Optional[CustomLogger]:
    """
    Initialize a custom logger compatible class
    """
    try:
        custom_logger_init_args = custom_logger_init_args or {}
        if logging_integration == "agentops":  # Add AgentOps initialization
            _v2 = _maybe_construct_otel_v2("agentops", _in_memory_loggers)
            if _v2 is not None:
                return _v2  # type: ignore
            for callback in _in_memory_loggers:
                if isinstance(callback, AgentOps):
                    return callback  # type: ignore

            agentops_logger = AgentOps()
            _in_memory_loggers.append(agentops_logger)
            return agentops_logger  # type: ignore
        elif logging_integration == "lago":
            for callback in _in_memory_loggers:
                if isinstance(callback, LagoLogger):
                    return callback  # type: ignore

            lago_logger = LagoLogger()
            _in_memory_loggers.append(lago_logger)
            return lago_logger  # type: ignore
        elif logging_integration == "openmeter":
            for callback in _in_memory_loggers:
                if isinstance(callback, OpenMeterLogger):
                    return callback  # type: ignore

            _openmeter_logger = OpenMeterLogger()
            _in_memory_loggers.append(_openmeter_logger)
            return _openmeter_logger  # type: ignore
        elif logging_integration == "posthog":
            for callback in _in_memory_loggers:
                if isinstance(callback, PostHogLogger):
                    return callback  # type: ignore

            _posthog_logger = PostHogLogger()
            _in_memory_loggers.append(_posthog_logger)
            return _posthog_logger  # type: ignore
        elif logging_integration == "braintrust":
            from litellm.integrations.braintrust_logging import BraintrustLogger

            for callback in _in_memory_loggers:
                if isinstance(callback, BraintrustLogger):
                    return callback  # type: ignore

            braintrust_logger = BraintrustLogger()
            _in_memory_loggers.append(braintrust_logger)
            return braintrust_logger  # type: ignore
        elif logging_integration == "langsmith":
            for callback in _in_memory_loggers:
                if isinstance(callback, LangsmithLogger):
                    return callback  # type: ignore

            _langsmith_logger = LangsmithLogger()
            _in_memory_loggers.append(_langsmith_logger)
            return _langsmith_logger  # type: ignore
        elif logging_integration == "argilla":
            for callback in _in_memory_loggers:
                if isinstance(callback, ArgillaLogger):
                    return callback  # type: ignore

            _argilla_logger = ArgillaLogger()
            _in_memory_loggers.append(_argilla_logger)
            return _argilla_logger  # type: ignore
        elif logging_integration == "literalai":
            for callback in _in_memory_loggers:
                if isinstance(callback, LiteralAILogger):
                    return callback  # type: ignore

            _literalai_logger = LiteralAILogger()
            _in_memory_loggers.append(_literalai_logger)
            return _literalai_logger  # type: ignore
        elif logging_integration == "litellm_agent":
            for callback in _in_memory_loggers:
                if isinstance(callback, LiteLLMAgentModelResolver):
                    return callback  # type: ignore

            _litellm_agent_resolver = LiteLLMAgentModelResolver()
            _in_memory_loggers.append(_litellm_agent_resolver)
            return _litellm_agent_resolver  # type: ignore
        elif logging_integration == "prometheus":
            PrometheusLogger = _get_cached_prometheus_logger()

            for callback in _in_memory_loggers:
                if isinstance(callback, PrometheusLogger):
                    return callback  # type: ignore

            _prometheus_logger = PrometheusLogger()
            _in_memory_loggers.append(_prometheus_logger)
            return _prometheus_logger  # type: ignore
        elif logging_integration == "datadog":
            # Check if team-scoped credentials are provided
            _dd_api_key = custom_logger_init_args.get("dd_api_key")
            _dd_site = custom_logger_init_args.get("dd_site")
            _dd_agent_host = custom_logger_init_args.get("dd_agent_host")
            _dd_agent_port = custom_logger_init_args.get("dd_agent_port")

            if _dd_api_key or _dd_site or _dd_agent_host:
                # Team-scoped credentials: use DynamicLoggingCache for per-credential isolation
                from litellm.integrations.datadog.datadog_team_handler import (
                    DataDogHandler,
                )

                return DataDogHandler.get_datadog_logger_for_request(
                    standard_callback_dynamic_params=custom_logger_init_args,  # type: ignore
                    in_memory_dynamic_logger_cache=in_memory_dynamic_logger_cache,
                )

            # Global (env-var based): reuse cached instance
            for callback in _in_memory_loggers:
                if isinstance(callback, DataDogLogger):
                    return callback  # type: ignore

            _datadog_logger = DataDogLogger()
            _in_memory_loggers.append(_datadog_logger)
            return _datadog_logger  # type: ignore
        elif logging_integration == "datadog_metrics":
            for callback in _in_memory_loggers:
                if isinstance(callback, DatadogMetricsLogger):
                    return callback  # type: ignore

            _datadog_metrics_logger = DatadogMetricsLogger()
            _in_memory_loggers.append(_datadog_metrics_logger)
            return _datadog_metrics_logger  # type: ignore
        elif logging_integration == "datadog_llm_observability":
            _datadog_llm_obs_logger = DataDogLLMObsLogger()
            _in_memory_loggers.append(_datadog_llm_obs_logger)
            return _datadog_llm_obs_logger  # type: ignore
        elif logging_integration == "azure_sentinel":
            for callback in _in_memory_loggers:
                if isinstance(callback, AzureSentinelLogger):
                    return callback  # type: ignore

            _azure_sentinel_logger = AzureSentinelLogger()
            _in_memory_loggers.append(_azure_sentinel_logger)
            return _azure_sentinel_logger  # type: ignore
        elif logging_integration == "gcs_bucket":
            for callback in _in_memory_loggers:
                if isinstance(callback, GCSBucketLogger):
                    return callback  # type: ignore

            _gcs_bucket_logger = GCSBucketLogger()
            _in_memory_loggers.append(_gcs_bucket_logger)
            return _gcs_bucket_logger  # type: ignore
        elif logging_integration == "s3_v2":
            for callback in _in_memory_loggers:
                if isinstance(callback, S3V2Logger):
                    return callback  # type: ignore

            _s3_v2_logger = S3V2Logger()
            _in_memory_loggers.append(_s3_v2_logger)
            return _s3_v2_logger  # type: ignore
        elif logging_integration == "aws_sqs":
            for callback in _in_memory_loggers:
                if isinstance(callback, SQSLogger):
                    return callback  # type: ignore

            _aws_sqs_logger = SQSLogger()
            _in_memory_loggers.append(_aws_sqs_logger)
            return _aws_sqs_logger  # type: ignore
        elif logging_integration == "azure_storage":
            for callback in _in_memory_loggers:
                if isinstance(callback, AzureBlobStorageLogger):
                    return callback  # type: ignore

            _azure_storage_logger = AzureBlobStorageLogger()
            _in_memory_loggers.append(_azure_storage_logger)
            return _azure_storage_logger  # type: ignore
        elif logging_integration == "opik":
            for callback in _in_memory_loggers:
                if isinstance(callback, OpikLogger):
                    return callback  # type: ignore

            _opik_logger = OpikLogger()
            _in_memory_loggers.append(_opik_logger)
            return _opik_logger  # type: ignore
        elif logging_integration == "arize":
            _v2 = _maybe_construct_otel_v2("arize", _in_memory_loggers)
            if _v2 is not None:
                return _v2  # type: ignore
            from litellm.integrations.opentelemetry import (
                OpenTelemetry,
                OpenTelemetryConfig,
            )

            arize_config = ArizeLogger.get_arize_config()
            if arize_config.endpoint is None:
                raise ValueError(
                    "No valid endpoint found for Arize, please set 'ARIZE_ENDPOINT' to your GRPC endpoint or 'ARIZE_HTTP_ENDPOINT' to your HTTP endpoint"
                )
            otel_config = OpenTelemetryConfig(
                exporter=arize_config.protocol,
                endpoint=arize_config.endpoint,
                service_name=arize_config.project_name,
            )

            os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"] = (
                f"space_id={arize_config.space_key or arize_config.space_id},api_key={arize_config.api_key}"
            )
            for callback in _in_memory_loggers:
                if (
                    isinstance(callback, ArizeLogger)
                    and callback.callback_name == "arize"
                ):
                    return callback  # type: ignore
            _arize_otel_logger = ArizeLogger(config=otel_config, callback_name="arize")
            _in_memory_loggers.append(_arize_otel_logger)
            return _arize_otel_logger  # type: ignore
        elif logging_integration == "arize_phoenix":
            _v2 = _maybe_construct_otel_v2("arize_phoenix", _in_memory_loggers)
            if _v2 is not None:
                return _v2  # type: ignore
            from litellm.integrations.opentelemetry import (
                OpenTelemetry,
                OpenTelemetryConfig,
            )

            arize_phoenix_config = ArizePhoenixLogger.get_arize_phoenix_config()
            otel_config = OpenTelemetryConfig(
                exporter=arize_phoenix_config.protocol,
                endpoint=arize_phoenix_config.endpoint,
                headers=arize_phoenix_config.otlp_auth_headers,
            )

            # auth can be disabled on local deployments of arize phoenix
            if arize_phoenix_config.otlp_auth_headers is not None:
                os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"] = (
                    arize_phoenix_config.otlp_auth_headers
                )

            for callback in _in_memory_loggers:
                if (
                    isinstance(callback, ArizePhoenixLogger)
                    and callback.callback_name == "arize_phoenix"
                ):
                    return callback  # type: ignore
            _arize_phoenix_otel_logger = ArizePhoenixLogger(
                config=otel_config, callback_name="arize_phoenix"
            )
            _in_memory_loggers.append(_arize_phoenix_otel_logger)
            return _arize_phoenix_otel_logger  # type: ignore
        elif logging_integration == "levo":
            _v2 = _maybe_construct_otel_v2("levo", _in_memory_loggers)
            if _v2 is not None:
                return _v2  # type: ignore
            from litellm.integrations.levo.levo import LevoLogger
            from litellm.integrations.opentelemetry import (
                OpenTelemetry,
                OpenTelemetryConfig,
            )

            levo_config = LevoLogger.get_levo_config()
            otel_config = OpenTelemetryConfig(
                exporter=levo_config.protocol,
                endpoint=levo_config.endpoint,
                headers=levo_config.otlp_auth_headers,
            )

            # Check if LevoLogger instance already exists
            for callback in _in_memory_loggers:
                if (
                    isinstance(callback, LevoLogger)
                    and callback.callback_name == "levo"
                ):
                    return callback  # type: ignore

            _levo_otel_logger = LevoLogger(config=otel_config, callback_name="levo")
            _in_memory_loggers.append(_levo_otel_logger)
            return _levo_otel_logger  # type: ignore
        elif logging_integration == "otel":
            # Gate the new typed V2 adapter behind LITELLM_OTEL_V2. When off,
            # the legacy 3,227-line god-class is used unchanged. The two are
            # never registered simultaneously — the dedup loop below treats
            # any module under ``litellm.integrations.otel`` or
            # ``litellm.integrations.opentelemetry`` as "the OTel callback".
            from litellm.integrations.otel.model.config import is_otel_v2_enabled

            if is_otel_v2_enabled():
                from litellm.integrations.otel.logger import OpenTelemetryV2

                for callback in _in_memory_loggers:
                    if type(callback) is OpenTelemetryV2:
                        return callback  # type: ignore
                otel_logger_v2 = OpenTelemetryV2(
                    **_get_custom_logger_settings_from_proxy_server(
                        callback_name=logging_integration
                    )
                )
                _in_memory_loggers.append(otel_logger_v2)
                _maybe_auto_initialize_arize_phoenix(_in_memory_loggers)
                return otel_logger_v2  # type: ignore

            from litellm.integrations.opentelemetry import OpenTelemetry

            for callback in _in_memory_loggers:
                if type(callback) is OpenTelemetry:
                    return callback  # type: ignore
            otel_logger = OpenTelemetry(
                **_get_custom_logger_settings_from_proxy_server(
                    callback_name=logging_integration
                )
            )
            _in_memory_loggers.append(otel_logger)

            # Auto-initialize Arize Phoenix if Phoenix env vars are configured
            # This allows users to get nested traces in both OTEL and Phoenix
            # by only specifying "otel" in callbacks
            _maybe_auto_initialize_arize_phoenix(_in_memory_loggers)

            return otel_logger  # type: ignore

        elif logging_integration == "galileo":
            for callback in _in_memory_loggers:
                if isinstance(callback, GalileoObserve):
                    return callback  # type: ignore

            galileo_logger = GalileoObserve()
            _in_memory_loggers.append(galileo_logger)
            return galileo_logger  # type: ignore
        elif logging_integration == "cloudzero":
            from litellm.integrations.cloudzero.cloudzero import CloudZeroLogger

            for callback in _in_memory_loggers:
                if isinstance(callback, CloudZeroLogger):
                    return callback  # type: ignore
            cloudzero_logger = CloudZeroLogger()
            _in_memory_loggers.append(cloudzero_logger)
            return cloudzero_logger  # type: ignore
        elif logging_integration == "focus":
            from litellm.integrations.focus.focus_logger import FocusLogger

            for callback in _in_memory_loggers:
                if (
                    type(callback) is FocusLogger
                ):  # exact match; exclude subclasses like VantageLogger
                    return callback  # type: ignore
            focus_logger = FocusLogger()
            _in_memory_loggers.append(focus_logger)
            return focus_logger  # type: ignore
        elif logging_integration == "mavvrik":
            from litellm.integrations.mavvrik_focus.mavvrik_focus_logger import (
                MavvrikFocusLogger,
            )

            for callback in _in_memory_loggers:
                if type(callback) is MavvrikFocusLogger:
                    return callback  # type: ignore
            mavvrik_focus_logger = MavvrikFocusLogger()
            _in_memory_loggers.append(mavvrik_focus_logger)
            return mavvrik_focus_logger  # type: ignore
        elif logging_integration == "vantage":
            from litellm.integrations.vantage.vantage_logger import VantageLogger

            for callback in _in_memory_loggers:
                if isinstance(callback, VantageLogger):
                    return callback  # type: ignore
            vantage_logger = VantageLogger()
            _in_memory_loggers.append(vantage_logger)
            return vantage_logger  # type: ignore
        elif logging_integration == "deepeval":
            for callback in _in_memory_loggers:
                if isinstance(callback, DeepEvalLogger):
                    return callback  # type: ignore
            deepeval_logger = DeepEvalLogger()
            _in_memory_loggers.append(deepeval_logger)
            return deepeval_logger  # type: ignore

        elif logging_integration == "logfire":
            if "LOGFIRE_TOKEN" not in os.environ:
                raise ValueError("LOGFIRE_TOKEN not found in environment variables")
            from litellm.integrations.opentelemetry import (
                OpenTelemetry,
                OpenTelemetryConfig,
            )

            logfire_base_url = os.getenv(
                "LOGFIRE_BASE_URL", "https://logfire-api.pydantic.dev"
            )
            otel_config = OpenTelemetryConfig(
                exporter="otlp_http",
                endpoint=f"{logfire_base_url.rstrip('/')}/v1/traces",
                headers=f"Authorization={os.getenv('LOGFIRE_TOKEN')}",
            )
            for callback in _in_memory_loggers:
                # Use exact type check to avoid matching ArizePhoenixLogger (subclass)
                if type(callback) is OpenTelemetry:
                    return callback  # type: ignore
            _otel_logger = OpenTelemetry(config=otel_config)
            _in_memory_loggers.append(_otel_logger)
            return _otel_logger  # type: ignore
        elif logging_integration == "dynamic_rate_limiter":
            from litellm.proxy.hooks.dynamic_rate_limiter import (
                _PROXY_DynamicRateLimitHandler,
            )

            for callback in _in_memory_loggers:
                if isinstance(callback, _PROXY_DynamicRateLimitHandler):
                    return callback  # type: ignore

            if internal_usage_cache is None:
                raise Exception(
                    "Internal Error: Cache cannot be empty - internal_usage_cache={}".format(
                        internal_usage_cache
                    )
                )

            dynamic_rate_limiter_obj = _PROXY_DynamicRateLimitHandler(
                internal_usage_cache=internal_usage_cache
            )

            if llm_router is not None and isinstance(llm_router, litellm.Router):
                dynamic_rate_limiter_obj.update_variables(llm_router=llm_router)
            _in_memory_loggers.append(dynamic_rate_limiter_obj)
            return dynamic_rate_limiter_obj  # type: ignore
        elif logging_integration == "dynamic_rate_limiter_v3":
            from litellm.proxy.hooks.dynamic_rate_limiter_v3 import (
                _PROXY_DynamicRateLimitHandlerV3,
            )

            for callback in _in_memory_loggers:
                if isinstance(callback, _PROXY_DynamicRateLimitHandlerV3):
                    return callback  # type: ignore

            if internal_usage_cache is None:
                raise Exception(
                    "Internal Error: Cache cannot be empty - internal_usage_cache={}".format(
                        internal_usage_cache
                    )
                )

            dynamic_rate_limiter_obj_v3 = _PROXY_DynamicRateLimitHandlerV3(
                internal_usage_cache=internal_usage_cache
            )

            if llm_router is not None and isinstance(llm_router, litellm.Router):
                dynamic_rate_limiter_obj_v3.update_variables(llm_router=llm_router)
            _in_memory_loggers.append(dynamic_rate_limiter_obj_v3)
            return dynamic_rate_limiter_obj_v3  # type: ignore
        elif logging_integration == "langtrace":
            if "LANGTRACE_API_KEY" not in os.environ:
                raise ValueError("LANGTRACE_API_KEY not found in environment variables")
            _v2 = _maybe_construct_otel_v2("langtrace", _in_memory_loggers)
            if _v2 is not None:
                return _v2  # type: ignore

            from litellm.integrations.opentelemetry import (
                OpenTelemetry,
                OpenTelemetryConfig,
            )

            otel_config = OpenTelemetryConfig(
                exporter="otlp_http",
                endpoint="https://langtrace.ai/api/trace",
            )
            os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"] = (
                f"api_key={os.getenv('LANGTRACE_API_KEY')}"
            )
            for callback in _in_memory_loggers:
                if (
                    isinstance(callback, OpenTelemetry)
                    and callback.callback_name == "langtrace"
                ):
                    return callback  # type: ignore
            _otel_logger = OpenTelemetry(config=otel_config, callback_name="langtrace")
            _in_memory_loggers.append(_otel_logger)
            return _otel_logger  # type: ignore

        elif logging_integration == "mlflow":
            for callback in _in_memory_loggers:
                if isinstance(callback, MlflowLogger):
                    return callback  # type: ignore

            _mlflow_logger = MlflowLogger()
            _in_memory_loggers.append(_mlflow_logger)
            return _mlflow_logger  # type: ignore
        elif logging_integration == "langfuse":
            for callback in _in_memory_loggers:
                if isinstance(callback, LangfusePromptManagement):
                    return callback

            langfuse_logger = LangfusePromptManagement()
            _in_memory_loggers.append(langfuse_logger)
            return langfuse_logger  # type: ignore
        elif logging_integration == "langfuse_otel":
            _v2 = _maybe_construct_otel_v2("langfuse_otel", _in_memory_loggers)
            if _v2 is not None:
                return _v2  # type: ignore
            from litellm.integrations.langfuse.langfuse_otel import LangfuseOtelLogger

            for callback in _in_memory_loggers:
                if (
                    isinstance(callback, LangfuseOtelLogger)
                    and callback.callback_name == "langfuse_otel"
                ):
                    return callback  # type: ignore
            # Allow LangfuseOtelLogger to initialize its own config safely
            # This prevents startup crashes if LANGFUSE keys are not in env (e.g. for dynamic usage)
            _otel_logger = LangfuseOtelLogger(
                config=None, callback_name="langfuse_otel"
            )
            _in_memory_loggers.append(_otel_logger)
            return _otel_logger  # type: ignore
        elif logging_integration == "weave_otel":
            _v2 = _maybe_construct_otel_v2("weave_otel", _in_memory_loggers)
            if _v2 is not None:
                return _v2  # type: ignore
            from litellm.integrations.opentelemetry import OpenTelemetryConfig
            from litellm.integrations.weave.weave_otel import (
                WeaveOtelLogger,
                get_weave_otel_config,
            )

            weave_otel_config = get_weave_otel_config()

            otel_config = OpenTelemetryConfig(
                exporter=weave_otel_config.protocol,
                endpoint=weave_otel_config.endpoint,
                headers=weave_otel_config.otlp_auth_headers,
            )

            for callback in _in_memory_loggers:
                if (
                    isinstance(callback, WeaveOtelLogger)
                    and callback.callback_name == "weave_otel"
                ):
                    return callback  # type: ignore
            _otel_logger = WeaveOtelLogger(
                config=otel_config, callback_name="weave_otel"
            )
            _in_memory_loggers.append(_otel_logger)
            return _otel_logger  # type: ignore
        elif logging_integration == "pagerduty":
            for callback in _in_memory_loggers:
                if isinstance(callback, PagerDutyAlerting):
                    return callback
            pagerduty_logger = PagerDutyAlerting(**custom_logger_init_args)
            _in_memory_loggers.append(pagerduty_logger)
            return pagerduty_logger  # type: ignore
        elif logging_integration == "anthropic_cache_control_hook":
            for callback in _in_memory_loggers:
                if isinstance(callback, AnthropicCacheControlHook):
                    return callback
            anthropic_cache_control_hook = AnthropicCacheControlHook()
            _in_memory_loggers.append(anthropic_cache_control_hook)
            return anthropic_cache_control_hook  # type: ignore
        elif logging_integration == "vector_store_pre_call_hook":
            from litellm.integrations.vector_store_integrations.vector_store_pre_call_hook import (
                VectorStorePreCallHook,
            )

            for callback in _in_memory_loggers:
                if isinstance(callback, VectorStorePreCallHook):
                    return callback
            vector_store_pre_call_hook = VectorStorePreCallHook()
            _in_memory_loggers.append(vector_store_pre_call_hook)
            return vector_store_pre_call_hook  # type: ignore
        elif logging_integration == "gcs_pubsub":
            for callback in _in_memory_loggers:
                if isinstance(callback, GcsPubSubLogger):
                    return callback
            _gcs_pubsub_logger = GcsPubSubLogger()
            _in_memory_loggers.append(_gcs_pubsub_logger)
            return _gcs_pubsub_logger  # type: ignore
        elif logging_integration == "generic_api":
            for callback in _in_memory_loggers:
                if isinstance(callback, GenericAPILogger):
                    return callback
            generic_api_logger = GenericAPILogger()
            _in_memory_loggers.append(generic_api_logger)
            return generic_api_logger  # type: ignore
        elif logging_integration == "resend_email":
            for callback in _in_memory_loggers:
                if isinstance(callback, ResendEmailLogger):
                    return callback
            resend_email_logger = ResendEmailLogger()
            _in_memory_loggers.append(resend_email_logger)
            return resend_email_logger  # type: ignore
        elif logging_integration == "sendgrid_email":
            for callback in _in_memory_loggers:
                if isinstance(callback, SendGridEmailLogger):
                    return callback
            sendgrid_email_logger = SendGridEmailLogger()
            _in_memory_loggers.append(sendgrid_email_logger)
            return sendgrid_email_logger  # type: ignore
        elif logging_integration == "smtp_email":
            for callback in _in_memory_loggers:
                if isinstance(callback, SMTPEmailLogger):
                    return callback
            smtp_email_logger = SMTPEmailLogger()
            _in_memory_loggers.append(smtp_email_logger)
            return smtp_email_logger  # type: ignore
        elif logging_integration == "humanloop":
            for callback in _in_memory_loggers:
                if isinstance(callback, HumanloopLogger):
                    return callback

            humanloop_logger = HumanloopLogger()
            _in_memory_loggers.append(humanloop_logger)
            return humanloop_logger  # type: ignore
        elif logging_integration == "dotprompt":
            for callback in _in_memory_loggers:
                if isinstance(callback, DotpromptManager):
                    return callback

            dotprompt_logger = DotpromptManager()
            _in_memory_loggers.append(dotprompt_logger)
            return dotprompt_logger  # type: ignore
        elif logging_integration == "bitbucket":
            from litellm.integrations.bitbucket.bitbucket_prompt_manager import (
                BitBucketPromptManager,
            )

            for callback in _in_memory_loggers:
                if isinstance(callback, BitBucketPromptManager):
                    return callback

            # Get global BitBucket config
            bitbucket_config = getattr(litellm, "global_bitbucket_config", None)
            if bitbucket_config is None:
                raise ValueError(
                    "BitBucket configuration not found. Please set litellm.global_bitbucket_config first."
                )

            bitbucket_logger = BitBucketPromptManager(bitbucket_config=bitbucket_config)
            _in_memory_loggers.append(bitbucket_logger)
            return bitbucket_logger  # type: ignore
        elif logging_integration == "gitlab":
            from litellm.integrations.gitlab.gitlab_prompt_manager import (
                GitLabPromptManager,
            )

            for callback in _in_memory_loggers:
                if isinstance(callback, GitLabPromptManager):
                    return callback

            # Get global BitBucket config
            gitlab_config = getattr(litellm, "global_gitlab_config", None)
            if gitlab_config is None:
                raise ValueError(
                    "Gitlab configuration not found. Please set litellm.global_gitlab_config first."
                )

            gitlab_logger = GitLabPromptManager(gitlab_config=gitlab_config)
            _in_memory_loggers.append(gitlab_logger)
            return gitlab_logger  # type: ignore
        elif logging_integration == "newrelic":
            for callback in _in_memory_loggers:
                if isinstance(callback, NewRelicLogger):
                    return callback  # type: ignore
            newrelic_logger = NewRelicLogger()
            _in_memory_loggers.append(newrelic_logger)
            return newrelic_logger  # type: ignore
        return None
    except Exception as e:
        verbose_logger.exception(
            f"[Non-Blocking Error] Error initializing custom logger: {e}"
        )
        return None
    return None

