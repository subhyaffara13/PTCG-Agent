
def log_guardrail_information(func):
    """
    Decorator to add standard logging guardrail information to any function

    Add this decorator to ensure your guardrail response is logged to DataDog, OTEL, s3, GCS etc.

    Logs for:
        - pre_call
        - during_call
        - post_call

    Some guardrails (e.g. ``block_code_execution``) call
    ``add_standard_logging_guardrail_information_to_request_data`` directly
    from inside the wrapped function so they can record a richer payload
    (structured detections, tracing detail) than this decorator's
    "allow"/"mask"/raw-response default. To avoid double-recording in that
    case (which would emit two spans, two Datadog records, two spend-log
    entries, etc.), snapshot the entry count before invocation: if the
    wrapped function already appended its own entry, skip the auto-record.
    """
    import functools
    import inspect

    def _infer_event_type_from_function_name(
        func_name: str,
    ) -> Optional[GuardrailEventHooks]:
        """Infer the actual event type from the function name"""
        if func_name == "async_pre_call_hook":
            return GuardrailEventHooks.pre_call
        elif func_name == "async_moderation_hook":
            return GuardrailEventHooks.during_call
        elif func_name in (
            "async_post_call_success_hook",
            "async_post_call_streaming_hook",
        ):
            return GuardrailEventHooks.post_call
        return None

    def _count_recorded_guardrail_entries(request_data: dict) -> int:
        total = 0
        for container_key in ("metadata", "litellm_metadata"):
            container = request_data.get(container_key)
            if isinstance(container, dict):
                entries = container.get("standard_logging_guardrail_information")
                if isinstance(entries, list):
                    total += len(entries)
        return total

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = datetime.now()  # Move start_time inside the wrapper
        self: CustomGuardrail = args[0]
        request_data: dict = kwargs.get("data") or kwargs.get("request_data") or {}
        event_type = _infer_event_type_from_function_name(func.__name__)

        # Store original inputs for comparison (for apply_guardrail functions)
        original_inputs = None
        if func.__name__ == "apply_guardrail" and "inputs" in kwargs:
            original_inputs = kwargs.get("inputs")

        entries_before = _count_recorded_guardrail_entries(request_data)
        try:
            response = await func(*args, **kwargs)
            if _count_recorded_guardrail_entries(request_data) > entries_before:
                return response
            return self._process_response(
                response=response,
                request_data=request_data,
                start_time=start_time.timestamp(),
                end_time=datetime.now().timestamp(),
                duration=(datetime.now() - start_time).total_seconds(),
                event_type=event_type,
                original_inputs=original_inputs,
            )
        except Exception as e:
            if _count_recorded_guardrail_entries(request_data) > entries_before:
                raise
            return self._process_error(
                e=e,
                request_data=request_data,
                start_time=start_time.timestamp(),
                end_time=datetime.now().timestamp(),
                duration=(datetime.now() - start_time).total_seconds(),
                event_type=event_type,
            )

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = datetime.now()  # Move start_time inside the wrapper
        self: CustomGuardrail = args[0]
        request_data: dict = kwargs.get("data") or kwargs.get("request_data") or {}
        event_type = _infer_event_type_from_function_name(func.__name__)

        # Store original inputs for comparison (for apply_guardrail functions)
        original_inputs = None
        if func.__name__ == "apply_guardrail" and "inputs" in kwargs:
            original_inputs = kwargs.get("inputs")

        entries_before = _count_recorded_guardrail_entries(request_data)
        try:
            response = func(*args, **kwargs)
            if _count_recorded_guardrail_entries(request_data) > entries_before:
                return response
            return self._process_response(
                response=response,
                request_data=request_data,
                duration=(datetime.now() - start_time).total_seconds(),
                event_type=event_type,
                original_inputs=original_inputs,
            )
        except Exception as e:
            if _count_recorded_guardrail_entries(request_data) > entries_before:
                raise
            return self._process_error(
                e=e,
                request_data=request_data,
                duration=(datetime.now() - start_time).total_seconds(),
                event_type=event_type,
            )

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if inspect.iscoroutinefunction(func):
            return async_wrapper(*args, **kwargs)
        return sync_wrapper(*args, **kwargs)

    return wrapper

