
def _resolve_audit_log_callback(name: str) -> Optional[CustomLogger]:
    """Resolve a string callback name to a CustomLogger instance, with caching.

    For "s3_v2" with `litellm.s3_audit_callback_params` set, constructs a
    dedicated `S3Logger` so audit logs can target a different bucket than the
    normal-log singleton served by `_init_custom_logger_compatible_class`.
    """
    if name in _audit_log_callback_cache:
        return _audit_log_callback_cache[name]

    instance: Optional[CustomLogger]
    if (
        name == "s3_v2"
        and getattr(litellm, "s3_audit_callback_params", None) is not None
    ):
        from litellm.integrations.s3_v2 import S3Logger as S3V2Logger

        instance = S3V2Logger(
            s3_callback_params_override=litellm.s3_audit_callback_params
        )
    else:
        from litellm.litellm_core_utils.litellm_logging import (
            _init_custom_logger_compatible_class,
        )

        instance = _init_custom_logger_compatible_class(
            logging_integration=name,  # type: ignore
            internal_usage_cache=None,
            llm_router=None,
        )

    if instance is not None:
        _audit_log_callback_cache[name] = instance
    return instance

