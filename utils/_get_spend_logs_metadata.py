
def _get_spend_logs_metadata(
    metadata: Optional[dict],
    applied_guardrails: Optional[List[str]] = None,
    batch_models: Optional[List[str]] = None,
    mcp_tool_call_metadata: Optional[StandardLoggingMCPToolCall] = None,
    vector_store_request_metadata: Optional[
        List[StandardLoggingVectorStoreRequest]
    ] = None,
    guardrail_information: Optional[List[StandardLoggingGuardrailInformation]] = None,
    usage_object: Optional[dict] = None,
    model_map_information: Optional[StandardLoggingModelInformation] = None,
    cold_storage_object_key: Optional[str] = None,
    litellm_overhead_time_ms: Optional[float] = None,
    cost_breakdown: Optional[CostBreakdown] = None,
) -> SpendLogsMetadata:
    if metadata is None:
        return SpendLogsMetadata(
            user_api_key=None,
            user_api_key_alias=None,
            user_api_key_team_id=None,
            user_api_key_project_id=None,
            user_api_key_project_alias=None,
            user_api_key_org_id=None,
            user_api_key_user_id=None,
            user_api_key_team_alias=None,
            spend_logs_metadata=None,
            requester_ip_address=None,
            additional_usage_values=None,
            applied_guardrails=None,
            status=None or "success",
            error_information=None,
            proxy_server_request=None,
            batch_models=None,
            mcp_tool_call_metadata=None,
            vector_store_request_metadata=None,
            model_map_information=None,
            usage_object=None,
            guardrail_information=None,
            eval_information=None,
            cold_storage_object_key=cold_storage_object_key,
            litellm_overhead_time_ms=None,
            attempted_retries=None,
            max_retries=None,
            cost_breakdown=None,
        )
    verbose_proxy_logger.debug(
        "getting payload for SpendLogs, available keys in metadata: "
        + str(list(metadata.keys()))
    )

    # Filter the metadata dictionary to include only the specified keys
    clean_metadata = SpendLogsMetadata(
        **{  # type: ignore
            key: metadata.get(key) for key in SpendLogsMetadata.__annotations__.keys()
        }
    )
    clean_metadata["applied_guardrails"] = applied_guardrails
    clean_metadata["batch_models"] = batch_models
    clean_metadata["mcp_tool_call_metadata"] = mcp_tool_call_metadata
    clean_metadata["vector_store_request_metadata"] = (
        _get_vector_store_request_for_spend_logs_payload(vector_store_request_metadata)
    )
    clean_metadata["guardrail_information"] = guardrail_information
    clean_metadata["usage_object"] = usage_object
    clean_metadata["model_map_information"] = model_map_information
    clean_metadata["cold_storage_object_key"] = cold_storage_object_key
    clean_metadata["litellm_overhead_time_ms"] = litellm_overhead_time_ms
    clean_metadata["cost_breakdown"] = cost_breakdown

    return clean_metadata

