import os
from typing import Optional

def get_custom_logger_compatible_class(
    logging_integration: _custom_logger_compatible_callbacks_literal,
) -> Optional[CustomLogger]:
    try:
        if logging_integration == "lago":
            for callback in _in_memory_loggers:
                if isinstance(callback, LagoLogger):
                    return callback
        elif logging_integration == "openmeter":
            for callback in _in_memory_loggers:
                if isinstance(callback, OpenMeterLogger):
                    return callback
        elif logging_integration == "braintrust":
            from litellm.integrations.braintrust_logging import BraintrustLogger

            for callback in _in_memory_loggers:
                if isinstance(callback, BraintrustLogger):
                    return callback
        elif logging_integration == "galileo":
            for callback in _in_memory_loggers:
                if isinstance(callback, GalileoObserve):
                    return callback
        elif logging_integration == "cloudzero":
            from litellm.integrations.cloudzero.cloudzero import CloudZeroLogger

            for callback in _in_memory_loggers:
                if isinstance(callback, CloudZeroLogger):
                    return callback
        elif logging_integration == "focus":
            from litellm.integrations.focus.focus_logger import FocusLogger

            for callback in _in_memory_loggers:
                if (
                    type(callback) is FocusLogger
                ):  # exact match; exclude subclasses like VantageLogger
                    return callback
        elif logging_integration == "vantage":
            from litellm.integrations.vantage.vantage_logger import VantageLogger

            for callback in _in_memory_loggers:
                if isinstance(callback, VantageLogger):
                    return callback
        elif logging_integration == "deepeval":
            for callback in _in_memory_loggers:
                if isinstance(callback, DeepEvalLogger):
                    return callback
        elif logging_integration == "langsmith":
            for callback in _in_memory_loggers:
                if isinstance(callback, LangsmithLogger):
                    return callback
        elif logging_integration == "argilla":
            for callback in _in_memory_loggers:
                if isinstance(callback, ArgillaLogger):
                    return callback
        elif logging_integration == "literalai":
            for callback in _in_memory_loggers:
                if isinstance(callback, LiteralAILogger):
                    return callback
        elif logging_integration == "litellm_agent":
            for callback in _in_memory_loggers:
                if isinstance(callback, LiteLLMAgentModelResolver):
                    return callback
        elif logging_integration == "prometheus":
            PrometheusLogger = _get_cached_prometheus_logger()
            for callback in _in_memory_loggers:
                if isinstance(callback, PrometheusLogger):
                    return callback
        elif logging_integration == "datadog":
            for callback in _in_memory_loggers:
                if isinstance(callback, DataDogLogger):
                    return callback
        elif logging_integration == "datadog_metrics":
            for callback in _in_memory_loggers:
                if isinstance(callback, DatadogMetricsLogger):
                    return callback
        elif logging_integration == "datadog_llm_observability":
            for callback in _in_memory_loggers:
                if isinstance(callback, DataDogLLMObsLogger):
                    return callback
        elif logging_integration == "azure_sentinel":
            for callback in _in_memory_loggers:
                if isinstance(callback, AzureSentinelLogger):
                    return callback
        elif logging_integration == "gcs_bucket":
            for callback in _in_memory_loggers:
                if isinstance(callback, GCSBucketLogger):
                    return callback
        elif logging_integration == "s3_v2":
            for callback in _in_memory_loggers:
                if isinstance(callback, S3V2Logger):
                    return callback
        elif logging_integration == "aws_sqs":
            for callback in _in_memory_loggers:
                if isinstance(callback, SQSLogger):
                    return callback
            _aws_sqs_logger = SQSLogger()
            _in_memory_loggers.append(_aws_sqs_logger)
            return _aws_sqs_logger  # type: ignore
        elif logging_integration == "azure_storage":
            for callback in _in_memory_loggers:
                if isinstance(callback, AzureBlobStorageLogger):
                    return callback
        elif logging_integration == "opik":
            for callback in _in_memory_loggers:
                if isinstance(callback, OpikLogger):
                    return callback
        elif logging_integration == "langfuse":
            for callback in _in_memory_loggers:
                if isinstance(callback, LangfusePromptManagement):
                    return callback
        elif logging_integration == "otel":
            from litellm.integrations.opentelemetry import OpenTelemetry

            for callback in _in_memory_loggers:
                # Use exact type check to avoid matching ArizePhoenixLogger (subclass)
                if type(callback) is OpenTelemetry:
                    return callback
        elif logging_integration == "arize":
            if "ARIZE_API_KEY" not in os.environ:
                raise ValueError("ARIZE_API_KEY not found in environment variables")
            for callback in _in_memory_loggers:
                if (
                    isinstance(callback, ArizeLogger)
                    and callback.callback_name == "arize"
                ):
                    return callback
        elif logging_integration == "logfire":
            if "LOGFIRE_TOKEN" not in os.environ:
                raise ValueError("LOGFIRE_TOKEN not found in environment variables")
            from litellm.integrations.opentelemetry import OpenTelemetry

            for callback in _in_memory_loggers:
                # Use exact type check to avoid matching ArizePhoenixLogger (subclass)
                if type(callback) is OpenTelemetry:
                    return callback  # type: ignore

        elif logging_integration == "dynamic_rate_limiter":
            from litellm.proxy.hooks.dynamic_rate_limiter import (
                _PROXY_DynamicRateLimitHandler,
            )

            for callback in _in_memory_loggers:
                if isinstance(callback, _PROXY_DynamicRateLimitHandler):
                    return callback  # type: ignore
        elif logging_integration == "dynamic_rate_limiter_v3":
            from litellm.proxy.hooks.dynamic_rate_limiter_v3 import (
                _PROXY_DynamicRateLimitHandlerV3,
            )

            for callback in _in_memory_loggers:
                if isinstance(callback, _PROXY_DynamicRateLimitHandlerV3):
                    return callback  # type: ignore

        elif logging_integration == "langtrace":
            from litellm.integrations.opentelemetry import OpenTelemetry

            if "LANGTRACE_API_KEY" not in os.environ:
                raise ValueError("LANGTRACE_API_KEY not found in environment variables")

            for callback in _in_memory_loggers:
                if (
                    isinstance(callback, OpenTelemetry)
                    and callback.callback_name == "langtrace"
                ):
                    return callback

        elif logging_integration == "mlflow":
            for callback in _in_memory_loggers:
                if isinstance(callback, MlflowLogger):
                    return callback
        elif logging_integration == "pagerduty":
            for callback in _in_memory_loggers:
                if isinstance(callback, PagerDutyAlerting):
                    return callback
        elif logging_integration == "anthropic_cache_control_hook":
            for callback in _in_memory_loggers:
                if isinstance(callback, AnthropicCacheControlHook):
                    return callback
        elif logging_integration == "vector_store_pre_call_hook":
            from litellm.integrations.vector_store_integrations.vector_store_pre_call_hook import (
                VectorStorePreCallHook,
            )

            for callback in _in_memory_loggers:
                if isinstance(callback, VectorStorePreCallHook):
                    return callback
        elif logging_integration == "gcs_pubsub":
            for callback in _in_memory_loggers:
                if isinstance(callback, GcsPubSubLogger):
                    return callback
        elif logging_integration == "generic_api":
            for callback in _in_memory_loggers:
                if isinstance(callback, GenericAPILogger):
                    return callback
        elif logging_integration == "resend_email":
            for callback in _in_memory_loggers:
                if isinstance(callback, ResendEmailLogger):
                    return callback
        elif logging_integration == "sendgrid_email":
            for callback in _in_memory_loggers:
                if isinstance(callback, SendGridEmailLogger):
                    return callback
        elif logging_integration == "smtp_email":
            for callback in _in_memory_loggers:
                if isinstance(callback, SMTPEmailLogger):
                    return callback
        elif logging_integration == "newrelic":
            for callback in _in_memory_loggers:
                if isinstance(callback, NewRelicLogger):
                    return callback
        return None

    except Exception as e:
        verbose_logger.exception(
            f"[Non-Blocking Error] Error getting custom logger: {e}"
        )
        return None

