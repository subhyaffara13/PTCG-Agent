
def get_standard_logging_object_payload(
    kwargs: Optional[dict],
    init_response_obj: Union[Any, BaseModel, dict],
    start_time: dt_object,
    end_time: dt_object,
    logging_obj: Logging,
    status: StandardLoggingPayloadStatus,
    error_str: Optional[str] = None,
    original_exception: Optional[Exception] = None,
    standard_built_in_tools_params: Optional[StandardBuiltInToolsParams] = None,
) -> Optional[StandardLoggingPayload]:
    try:
        kwargs = kwargs or {}

        response_obj, hidden_params = _extract_response_obj_and_hidden_params(
            init_response_obj, original_exception
        )

        # standardize this function to be used across, s3, dynamoDB, langfuse logging
        litellm_params = kwargs.get("litellm_params", {}) or {}
        proxy_server_request = litellm_params.get("proxy_server_request") or {}

        # Merge both litellm_metadata and metadata to get complete metadata
        metadata: dict = StandardLoggingPayloadSetup.merge_litellm_metadata(
            litellm_params
        )

        completion_start_time = kwargs.get("completion_start_time", end_time)
        call_type = kwargs.get("call_type")
        cache_hit = kwargs.get("cache_hit", False)
        # Extract usage as a plain dict, avoiding Pydantic round-trip
        usage_dict = StandardLoggingPayloadSetup.get_usage_as_dict(
            response_obj=response_obj,
            combined_usage_object=cast(
                Optional[Usage], kwargs.get("combined_usage_object")
            ),
        )

        id = response_obj.get("id", kwargs.get("litellm_call_id"))

        _model_id = metadata.get("model_info", {}).get("id", "")
        _model_group = metadata.get("model_group", "")

        request_tags = StandardLoggingPayloadSetup._get_request_tags(
            litellm_params=litellm_params, proxy_server_request=proxy_server_request
        )

        # cleanup timestamps
        (
            start_time_float,
            end_time_float,
            completion_start_time_float,
        ) = StandardLoggingPayloadSetup.cleanup_timestamps(
            start_time=start_time,
            end_time=end_time,
            completion_start_time=completion_start_time,
        )
        response_time = StandardLoggingPayloadSetup.get_response_time(
            start_time_float=start_time_float,
            end_time_float=end_time_float,
            completion_start_time_float=completion_start_time_float,
            stream=kwargs.get("stream", False),
        )
        # clean up litellm metadata
        clean_metadata = StandardLoggingPayloadSetup.get_standard_logging_metadata(
            metadata=metadata,
            litellm_params=litellm_params,
            prompt_integration=kwargs.get("prompt_integration", None),
            applied_guardrails=kwargs.get("applied_guardrails", None),
            mcp_tool_call_metadata=kwargs.get("mcp_tool_call_metadata", None),
            vector_store_request_metadata=kwargs.get(
                "vector_store_request_metadata", None
            ),
            usage_object=usage_dict,
            proxy_server_request=proxy_server_request,
            start_time=start_time,
            response_id=id,
        )
        _request_body = proxy_server_request.get("body", {})
        end_user_id = clean_metadata["user_api_key_end_user_id"] or _request_body.get(
            "user", None
        )  # maintain backwards compatibility with old request body check

        saved_cache_cost: float = 0.0
        if cache_hit is True:
            id = f"{id}_cache_hit{time.time()}"  # do not duplicate the request id
            saved_cache_cost = (
                logging_obj._response_cost_calculator(
                    result=init_response_obj, cache_hit=False  # type: ignore
                )
                or 0.0
            )

        ## Get model cost information ##
        base_model = _get_base_model_from_metadata(model_call_details=kwargs)
        custom_pricing = use_custom_pricing_for_model(litellm_params=litellm_params)
        raw_response_cost = kwargs.get("response_cost")
        response_cost: float = raw_response_cost or 0.0

        # clean up litellm hidden params
        clean_hidden_params = StandardLoggingPayloadSetup.get_hidden_params(
            hidden_params
        )
        if (
            clean_hidden_params["response_cost"] is None
            and raw_response_cost is not None
        ):
            clean_hidden_params["response_cost"] = response_cost

        model_cost_information = StandardLoggingPayloadSetup.get_model_cost_information(
            base_model=base_model,
            custom_pricing=custom_pricing,
            custom_llm_provider=kwargs.get("custom_llm_provider"),
            init_response_obj=init_response_obj,
            api_base=litellm_params.get("api_base"),
        )

        error_information, error_str = (
            StandardLoggingPayloadSetup.get_error_information_for_logging_payload(
                metadata=metadata,
                original_exception=original_exception,
                error_str=error_str,
            )
        )

        ## get final response object ##
        final_response_obj = StandardLoggingPayloadSetup.get_final_response_obj(
            response_obj=response_obj,
            init_response_obj=init_response_obj,
            kwargs=kwargs,
        )

        stream: Optional[bool] = None
        if (
            kwargs.get("complete_streaming_response") is not None
            or kwargs.get("async_complete_streaming_response") is not None
        ) and kwargs.get("stream") is True:
            stream = True

        # Reconstruct full model name with provider prefix for logging
        # This ensures Bedrock models like "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
        # are logged as "bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0"
        custom_llm_provider = cast(Optional[str], kwargs.get("custom_llm_provider"))
        model_name = reconstruct_model_name(
            kwargs.get("model", "") or "", custom_llm_provider, metadata
        )
        response_model_name: Optional[str] = None
        if isinstance(final_response_obj, dict):
            response_model_name = final_response_obj.get("model")

        # For Azure Model Router, preserve the actual model in the top-level standard
        # logging payload only when the user has opted in.
        requested_model = kwargs.get("model")
        if (
            isinstance(requested_model, str)
            and (
                "model_router" in requested_model.lower()
                or "model-router" in requested_model.lower()
            )
            and isinstance(response_model_name, str)
            and response_model_name
        ):
            model_name = response_model_name

        payload: StandardLoggingPayload = StandardLoggingPayload(
            id=str(id),
            litellm_call_id=kwargs.get("litellm_call_id")
            or litellm_params.get("litellm_call_id"),
            trace_id=StandardLoggingPayloadSetup._get_standard_logging_payload_trace_id(
                logging_obj=logging_obj,
                litellm_params=litellm_params,
            ),
            call_type=call_type or "",
            cache_hit=cache_hit,
            stream=stream,
            status=status,
            status_fields=_get_status_fields(
                status=status,
                guardrail_information=metadata.get(
                    "standard_logging_guardrail_information", None
                ),
                error_str=error_str,
            ),
            custom_llm_provider=custom_llm_provider,
            saved_cache_cost=saved_cache_cost,
            startTime=start_time_float,
            endTime=end_time_float,
            completionStartTime=completion_start_time_float,
            response_time=response_time,
            model=model_name,
            metadata=clean_metadata,
            cache_key=clean_hidden_params["cache_key"],
            response_cost=response_cost,
            cost_breakdown=logging_obj.cost_breakdown,
            total_tokens=usage_dict.get("total_tokens", 0),
            prompt_tokens=usage_dict.get("prompt_tokens", 0),
            completion_tokens=usage_dict.get("completion_tokens", 0),
            request_tags=request_tags,
            end_user=end_user_id or "",
            api_base=StandardLoggingPayloadSetup.strip_trailing_slash(
                litellm_params.get("api_base", "")
            )
            or "",
            model_group=_model_group,
            model_id=_model_id,
            requester_ip_address=clean_metadata.get("requester_ip_address", None),
            user_agent=clean_metadata.get("user_agent", None),
            messages=truncate_base64_in_messages(
                StandardLoggingPayloadSetup.append_system_prompt_messages(
                    kwargs=kwargs, messages=kwargs.get("messages")
                )
            ),
            response=final_response_obj,
            model_parameters=ModelParamHelper.get_standard_logging_model_parameters(
                kwargs.get("optional_params", None) or {}
            ),
            hidden_params=clean_hidden_params,
            model_map_information=model_cost_information,
            error_str=error_str,
            error_information=error_information,
            response_cost_failure_debug_info=kwargs.get(
                "response_cost_failure_debug_information"
            ),
            guardrail_information=metadata.get(
                "standard_logging_guardrail_information", None
            ),
            standard_built_in_tools_params=standard_built_in_tools_params,
        )

        # emit_standard_logging_payload(payload) - Moved to success_handler to prevent double emitting

        return payload
    except Exception as e:
        verbose_logger.exception(
            "Error creating standard logging object - {}".format(str(e))
        )
        return None

