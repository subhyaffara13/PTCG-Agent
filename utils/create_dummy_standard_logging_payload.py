
def create_dummy_standard_logging_payload() -> StandardLoggingPayload:
    # First create the nested objects with proper typing
    model_info = StandardLoggingModelInformation(
        model_map_key="gpt-3.5-turbo", model_map_value=None
    )

    metadata = StandardLoggingMetadata(  # type: ignore
        user_api_key_hash=str("test_hash"),
        user_api_key_alias=str("test_alias"),
        user_api_key_team_id=str("test_team"),
        user_api_key_user_id=str("test_user"),
        user_api_key_team_alias=str("test_team_alias"),
        user_api_key_org_id=None,
        spend_logs_metadata=None,
        requester_ip_address=str("127.0.0.1"),
        requester_metadata=None,
        user_api_key_end_user_id=str("test_end_user"),
    )

    hidden_params = StandardLoggingHiddenParams(
        model_id=None,
        cache_key=None,
        api_base=None,
        response_cost=None,
        additional_headers=None,
        litellm_overhead_time_ms=None,
        batch_models=None,
        litellm_model_name=None,
        usage_object=None,
    )

    # Convert numeric values to appropriate types
    response_cost = Decimal("0.1")
    start_time = Decimal("1234567890.0")
    end_time = Decimal("1234567891.0")
    completion_start_time = Decimal("1234567890.5")
    saved_cache_cost = Decimal("0.0")

    # Create messages and response with proper typing
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, world!"}]
    response: Dict[str, List[Dict[str, Dict[str, str]]]] = {
        "choices": [{"message": {"content": "Hi there!"}}]
    }

    # Main payload initialization
    return StandardLoggingPayload(  # type: ignore
        id=str("test_id"),
        call_type=str("completion"),
        stream=bool(False),
        response_cost=response_cost,
        response_cost_failure_debug_info=None,
        status=str("success"),
        total_tokens=int(
            DEFAULT_MOCK_RESPONSE_PROMPT_TOKEN_COUNT
            + DEFAULT_MOCK_RESPONSE_COMPLETION_TOKEN_COUNT
        ),
        prompt_tokens=int(DEFAULT_MOCK_RESPONSE_PROMPT_TOKEN_COUNT),
        completion_tokens=int(DEFAULT_MOCK_RESPONSE_COMPLETION_TOKEN_COUNT),
        startTime=start_time,
        endTime=end_time,
        completionStartTime=completion_start_time,
        model_map_information=model_info,
        model=str("gpt-3.5-turbo"),
        model_id=str("model-123"),
        model_group=str("openai-gpt"),
        custom_llm_provider=str("openai"),
        api_base=str("https://api.openai.com"),
        metadata=metadata,
        cache_hit=bool(False),
        cache_key=None,
        saved_cache_cost=saved_cache_cost,
        request_tags=[],
        end_user=None,
        requester_ip_address=str("127.0.0.1"),
        messages=messages,
        response=response,
        error_str=None,
        model_parameters={"stream": True},
        hidden_params=hidden_params,
    )

