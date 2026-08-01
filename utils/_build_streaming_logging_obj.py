
def _build_streaming_logging_obj(
    request: "SendStreamingMessageRequest",
    agent_name: str,
    agent_id: Optional[str],
    litellm_params: Optional[Dict[str, Any]],
    metadata: Optional[Dict[str, Any]],
    proxy_server_request: Optional[Dict[str, Any]],
) -> Logging:
    """Build logging object for streaming A2A requests."""
    start_time = datetime.datetime.now()
    model = f"a2a_agent/{agent_name}"

    logging_obj = Logging(
        model=model,
        messages=[{"role": "user", "content": "streaming-request"}],
        stream=False,
        call_type="asend_message_streaming",
        start_time=start_time,
        litellm_call_id=str(request.id),
        function_id=str(request.id),
    )
    logging_obj.model = model
    logging_obj.custom_llm_provider = "a2a_agent"
    logging_obj.model_call_details["model"] = model
    logging_obj.model_call_details["custom_llm_provider"] = "a2a_agent"
    if agent_id:
        logging_obj.model_call_details["agent_id"] = agent_id

    _litellm_params = litellm_params.copy() if litellm_params else {}
    if metadata:
        _litellm_params["metadata"] = metadata
    if proxy_server_request:
        _litellm_params["proxy_server_request"] = proxy_server_request

    logging_obj.litellm_params = _litellm_params
    logging_obj.optional_params = _litellm_params
    logging_obj.model_call_details["litellm_params"] = _litellm_params
    logging_obj.model_call_details["metadata"] = metadata or {}

    return logging_obj

