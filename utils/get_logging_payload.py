from typing import Optional

def get_logging_payload(kwargs, response_obj, start_time, end_time) -> SpendLogsPayload:
    if kwargs is None:
        kwargs = {}

    if response_obj is None:
        response_obj = {}
    elif not isinstance(response_obj, BaseModel) and not isinstance(response_obj, dict):
        response_obj = {"result": str(response_obj)}
    # standardize this function to be used across, s3, dynamoDB, langfuse logging
    litellm_params = kwargs.get("litellm_params", {})
    metadata = get_litellm_metadata_from_kwargs(kwargs)
    completion_start_time = kwargs.get("completion_start_time", end_time)
    call_type = kwargs.get("call_type")
    cache_hit = kwargs.get("cache_hit", False)

    # Convert response_obj to dict first
    if isinstance(response_obj, dict):
        response_obj_dict = response_obj
    elif isinstance(response_obj, BaseModel):
        response_obj_dict = response_obj.model_dump()
    else:
        response_obj_dict = {}

    # Handle OCR responses which use usage_info instead of usage
    usage: dict = {}
    if call_type in ["ocr", "aocr"]:
        usage = _extract_usage_for_ocr_call(response_obj, response_obj_dict)
    else:
        # Use response_obj_dict instead of response_obj to avoid calling .get() on Pydantic models
        _usage = response_obj_dict.get("usage", None) or {}
        if isinstance(_usage, litellm.Usage):
            usage = dict(_usage)
        elif isinstance(_usage, dict):
            usage = _usage

    # A request that failed mid-stream has no usable response_obj usage, but the
    # streaming handler may have recovered the usage from the chunks already
    # delivered. Honor that override so the partial usage lands in spend tracking.
    _combined_usage = kwargs.get("combined_usage_object")
    if not usage and isinstance(_combined_usage, litellm.Usage):
        usage = _combined_usage.model_dump()

    id = get_spend_logs_id(call_type or "acompletion", response_obj_dict, kwargs)
    standard_logging_payload = cast(
        Optional[StandardLoggingPayload], kwargs.get("standard_logging_object", None)
    )

    end_user_id = get_end_user_id_for_cost_tracking(litellm_params)

    api_key = metadata.get("user_api_key", "")

    standard_logging_prompt_tokens: int = 0
    standard_logging_completion_tokens: int = 0
    standard_logging_total_tokens: int = 0
    if standard_logging_payload is not None:
        standard_logging_prompt_tokens = standard_logging_payload.get(
            "prompt_tokens", 0
        )
        standard_logging_completion_tokens = standard_logging_payload.get(
            "completion_tokens", 0
        )
        standard_logging_total_tokens = standard_logging_payload.get("total_tokens", 0)
    if api_key is not None and isinstance(api_key, str):
        if api_key.startswith("sk-"):
            # hash the api_key
            api_key = hash_token(api_key)

    if (
        standard_logging_payload is not None
    ):  # [TODO] migrate completely to sl payload. currently missing pass-through endpoint data
        api_key = (
            api_key
            or standard_logging_payload["metadata"].get("user_api_key_hash")
            or ""
        )
        end_user_id = end_user_id or standard_logging_payload["metadata"].get(
            "user_api_key_end_user_id"
        )
    # BUG FIX: Don't overwrite api_key when standard_logging_payload is None
    # The api_key was already extracted from metadata (line 243) and hashed (lines 256-259)
    request_tags = (
        safe_dumps(metadata.get("tags", []))
        if isinstance(metadata.get("tags", []), list)
        else "[]"
    )
    if (
        standard_logging_payload is not None
        and standard_logging_payload.get("request_tags") is not None
    ):  # use 'tags' from standard logging payload instead
        request_tags = safe_dumps(standard_logging_payload["request_tags"])

    _model_id = metadata.get("model_info", {}).get("id", "")
    _model_group = metadata.get("model_group", "")

    # Extract overhead from hidden_params if available
    litellm_overhead_time_ms = None
    if standard_logging_payload is not None:
        hidden_params = standard_logging_payload.get("hidden_params", {})
        litellm_overhead_time_ms = hidden_params.get("litellm_overhead_time_ms")

    # clean up litellm metadata
    clean_metadata = _get_spend_logs_metadata(
        metadata,
        applied_guardrails=(
            standard_logging_payload["metadata"].get("applied_guardrails", None)
            if standard_logging_payload is not None
            else None
        ),
        batch_models=(
            standard_logging_payload.get("hidden_params", {}).get("batch_models", None)
            if standard_logging_payload is not None
            else None
        ),
        mcp_tool_call_metadata=(
            standard_logging_payload["metadata"].get("mcp_tool_call_metadata", None)
            if standard_logging_payload is not None
            else None
        ),
        vector_store_request_metadata=(
            standard_logging_payload["metadata"].get(
                "vector_store_request_metadata", None
            )
            if standard_logging_payload is not None
            else None
        ),
        usage_object=(
            standard_logging_payload["metadata"].get("usage_object", None)
            if standard_logging_payload is not None
            else None
        ),
        model_map_information=(
            standard_logging_payload["model_map_information"]
            if standard_logging_payload is not None
            else None
        ),
        guardrail_information=(
            standard_logging_payload.get("guardrail_information", None)
            if standard_logging_payload is not None
            else (
                metadata.get("standard_logging_guardrail_information", None)
                if metadata is not None
                else None
            )
        ),
        cold_storage_object_key=(
            standard_logging_payload["metadata"].get("cold_storage_object_key", None)
            if standard_logging_payload is not None
            else None
        ),
        litellm_overhead_time_ms=litellm_overhead_time_ms,
        cost_breakdown=(
            standard_logging_payload.get("cost_breakdown", None)
            if standard_logging_payload is not None
            else None
        ),
    )

    special_usage_fields = ["completion_tokens", "prompt_tokens", "total_tokens"]
    additional_usage_values = {}
    for k, v in usage.items():
        if k not in special_usage_fields:
            if isinstance(v, BaseModel):
                v = v.model_dump()
            additional_usage_values.update({k: v})
    clean_metadata["additional_usage_values"] = additional_usage_values

    if litellm.cache is not None:
        cache_key = litellm.cache.get_cache_key(**kwargs)
    else:
        cache_key = "Cache OFF"
    if cache_hit is True:
        import time

        id = f"{id}_cache_hit{time.time()}"  # SpendLogs does not allow duplicate request_id

    mcp_namespaced_tool_name = None
    mcp_tool_call_metadata: Optional[StandardLoggingMCPToolCall] = clean_metadata.get(
        "mcp_tool_call_metadata"
    )
    if mcp_tool_call_metadata is not None:
        mcp_namespaced_tool_name = mcp_tool_call_metadata.get(
            "namespaced_tool_name", None
        )

    # Extract agent_id for A2A requests (set directly on model_call_details)
    agent_id: Optional[str] = kwargs.get("agent_id") or metadata.get("agent_id")
    custom_llm_provider = kwargs.get("custom_llm_provider")
    raw_model = cast(str, kwargs.get("model") or "")
    model_name = reconstruct_model_name(raw_model, custom_llm_provider, metadata or {})

    try:
        payload: SpendLogsPayload = SpendLogsPayload(
            request_id=str(id),
            call_type=call_type or "",
            api_key=str(api_key),
            cache_hit=str(cache_hit),
            startTime=_ensure_datetime_utc(start_time),
            endTime=_ensure_datetime_utc(end_time),
            completionStartTime=_ensure_datetime_utc(completion_start_time),
            model=model_name,
            user=metadata.get("user_api_key_user_id", "") or "",
            team_id=metadata.get("user_api_key_team_id", "") or "",
            organization_id=metadata.get("user_api_key_org_id") or "",
            metadata=safe_dumps(clean_metadata),
            cache_key=cache_key,
            spend=kwargs.get("response_cost", 0),
            total_tokens=usage.get("total_tokens", standard_logging_total_tokens),
            prompt_tokens=usage.get("prompt_tokens", standard_logging_prompt_tokens),
            completion_tokens=usage.get(
                "completion_tokens", standard_logging_completion_tokens
            ),
            request_tags=request_tags,
            end_user=end_user_id or "",
            api_base=litellm_params.get("api_base", ""),
            model_group=_model_group,
            model_id=_model_id,
            mcp_namespaced_tool_name=mcp_namespaced_tool_name,
            agent_id=agent_id,
            requester_ip_address=clean_metadata.get("requester_ip_address", None),
            custom_llm_provider=kwargs.get("custom_llm_provider", ""),
            messages=_get_messages_for_spend_logs_payload(
                standard_logging_payload=standard_logging_payload, metadata=metadata
            ),
            response=_get_response_for_spend_logs_payload(
                payload=standard_logging_payload, kwargs=kwargs
            ),
            proxy_server_request=_get_proxy_server_request_for_spend_logs_payload(
                metadata=metadata, litellm_params=litellm_params, kwargs=kwargs
            ),
            session_id=_get_session_id_for_spend_log(
                kwargs=kwargs,
                standard_logging_payload=standard_logging_payload,
            ),
            request_duration_ms=_get_request_duration_ms(start_time, end_time),
            status=_get_status_for_spend_log(
                metadata=metadata,
            ),
        )

        verbose_proxy_logger.debug(
            "SpendTable: created payload - request_id: %s, model: %s, spend: %s",
            payload.get("request_id"),
            payload.get("model"),
            payload.get("spend"),
        )

        # Explicitly clear large intermediate objects to reduce memory pressure
        del response_obj_dict, usage, clean_metadata, additional_usage_values

        return payload
    except Exception as e:
        spend_log_error("Error creating spendlogs object - %s", str(e), exc=e)
        raise e

