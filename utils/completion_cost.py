import logging
from typing import List, Optional, Union

def completion_cost(
    completion_response=None,
    model: Optional[str] = None,
    prompt="",
    messages: List = [],
    completion="",
    total_time: Optional[float] = 0.0,  # used for replicate, sagemaker
    call_type: Optional[CallTypesLiteral] = None,
    ### REGION ###
    custom_llm_provider=None,
    region_name=None,  # used for bedrock pricing
    ### IMAGE GEN ###
    size: Optional[str] = None,
    quality: Optional[str] = None,
    n: Optional[int] = None,  # number of images
    ### CUSTOM PRICING ###
    custom_cost_per_token: Optional[CostPerToken] = None,
    custom_cost_per_second: Optional[float] = None,
    optional_params: Optional[dict] = None,
    custom_pricing: Optional[bool] = None,
    base_model: Optional[str] = None,
    standard_built_in_tools_params: Optional[StandardBuiltInToolsParams] = None,
    litellm_model_name: Optional[str] = None,
    router_model_id: Optional[str] = None,
    litellm_logging_obj: Optional[LitellmLoggingObject] = None,
    ### SERVICE TIER ###
    service_tier: Optional[str] = None,  # for OpenAI service tier pricing
    ### DATA RESIDENCY ###
    data_residency: Optional[
        str
    ] = None,  # for OpenAI regional-processing uplift (e.g. "eu", "us")
) -> float:
    """
    Calculate the cost of a given completion call fot GPT-3.5-turbo, llama2, any litellm supported llm.

    Parameters:
        completion_response (litellm.ModelResponses): [Required] The response received from a LiteLLM completion request.

        [OPTIONAL PARAMS]
        model (str): Optional. The name of the language model used in the completion calls
        prompt (str): Optional. The input prompt passed to the llm
        completion (str): Optional. The output completion text from the llm
        total_time (float, int): Optional. (Only used for Replicate LLMs) The total time used for the request in seconds
        custom_cost_per_token: Optional[CostPerToken]: the cost per input + output token for the llm api call.
        custom_cost_per_second: Optional[float]: the cost per second for the llm api call.

    Returns:
        float: The cost in USD dollars for the completion based on the provided parameters.

    Exceptions:
        Raises exception if model not in the litellm model cost map. Register model, via custom pricing or PR - https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json


    Note:
        - If completion_response is provided, the function extracts token information and the model name from it.
        - If completion_response is not provided, the function calculates token counts based on the model and input text.
        - The cost is calculated based on the model, prompt tokens, and completion tokens.
        - For certain models containing "togethercomputer" in the name, prices are based on the model size.
        - For un-mapped Replicate models, the cost is calculated based on the total time used for the request.
    """
    try:
        call_type = _infer_call_type(call_type, completion_response) or "completion"

        if (
            (call_type == "aimage_generation" or call_type == "image_generation")
            and model is not None
            and isinstance(model, str)
            and len(model) == 0
            and custom_llm_provider == "azure"
        ):
            model = "dall-e-2"  # for dall-e-2, azure expects an empty model name
        # Handle Inputs to completion_cost
        prompt_tokens = 0
        prompt_characters: Optional[int] = None
        completion_tokens = 0
        completion_characters: Optional[int] = None
        cache_creation_input_tokens: Optional[int] = None
        cache_read_input_tokens: Optional[int] = None
        audio_transcription_file_duration: float = 0.0
        cost_per_token_usage_object: Optional[Usage] = _get_usage_object(
            completion_response=completion_response
        )
        rerank_billed_units: Optional[RerankBilledUnits] = None

        # Extract service_tier from optional_params if not provided directly
        if service_tier is None and optional_params is not None:
            service_tier = optional_params.get("service_tier")

        service_tier = _normalize_service_tier(service_tier)

        # Extract service_tier from completion_response if not provided
        if service_tier is None and completion_response is not None:
            if isinstance(completion_response, BaseModel):
                service_tier = getattr(completion_response, "service_tier", None)
            elif isinstance(completion_response, dict):
                service_tier = completion_response.get("service_tier")

        service_tier = _normalize_service_tier(service_tier)

        # Extract service_tier from usage object if not provided
        if service_tier is None and cost_per_token_usage_object is not None:
            if isinstance(cost_per_token_usage_object, BaseModel):
                service_tier = getattr(
                    cost_per_token_usage_object, "service_tier", None
                )
            elif isinstance(cost_per_token_usage_object, dict):
                service_tier = cost_per_token_usage_object.get("service_tier")

        service_tier = _normalize_service_tier(service_tier)

        selected_model = _select_model_name_for_cost_calc(
            model=model,
            completion_response=completion_response,
            custom_llm_provider=custom_llm_provider,
            custom_pricing=custom_pricing,
            base_model=base_model,
            router_model_id=router_model_id,
        )

        potential_model_names = [
            selected_model,
            _get_response_model(completion_response),
        ]
        if model is not None:
            potential_model_names.append(model)

        for idx, model in enumerate(potential_model_names):
            try:
                if verbose_logger.isEnabledFor(logging.DEBUG):
                    verbose_logger.debug(
                        f"selected model name for cost calculation: {model}"
                    )

                if completion_response is not None and (
                    isinstance(completion_response, BaseModel)
                    or isinstance(completion_response, dict)
                ):  # tts returns a custom class
                    if isinstance(completion_response, dict):
                        usage_obj: Optional[Union[dict, Usage]] = (
                            completion_response.get("usage", {})
                        )
                    else:
                        usage_obj = getattr(completion_response, "usage", {})
                    if isinstance(usage_obj, BaseModel) and not _is_known_usage_objects(
                        usage_obj=usage_obj
                    ):
                        _usage_for_dump = cast(BaseModel, usage_obj)
                        setattr(
                            completion_response,
                            "usage",
                            litellm.Usage(**_usage_for_dump.model_dump()),
                        )
                    if usage_obj is None:
                        _usage = {}
                    elif isinstance(usage_obj, BaseModel):
                        _usage = cast(BaseModel, usage_obj).model_dump()
                    else:
                        _usage = usage_obj

                    if ResponseAPILoggingUtils._is_response_api_usage(_usage):
                        _usage = ResponseAPILoggingUtils._transform_response_api_usage_to_chat_usage(
                            _usage
                        ).model_dump()
                    elif TranscriptionUsageObjectTransformation.is_transcription_usage_object(
                        _usage
                    ):
                        tr_usage = TranscriptionUsageObjectTransformation.transform_transcription_usage_object(
                            cast(
                                Union[
                                    TranscriptionUsageDurationObject,
                                    TranscriptionUsageTokensObject,
                                ],
                                _usage,
                            )
                        )
                        if tr_usage is not None:
                            _usage = tr_usage.model_dump()
                    else:
                        _usage = _usage

                    # get input/output tokens from completion_response
                    prompt_tokens = _usage.get("prompt_tokens", 0)
                    completion_tokens = _usage.get("completion_tokens", 0)
                    cache_creation_input_tokens = _usage.get(
                        "cache_creation_input_tokens", 0
                    )
                    cache_read_input_tokens = _usage.get("cache_read_input_tokens", 0)
                    if (
                        "prompt_tokens_details" in _usage
                        and _usage["prompt_tokens_details"] != {}
                        and _usage["prompt_tokens_details"]
                    ):
                        prompt_tokens_details = (
                            _usage.get("prompt_tokens_details") or {}
                        )
                        cache_read_input_tokens = prompt_tokens_details.get(
                            "cached_tokens", 0
                        )

                    total_time = getattr(completion_response, "_response_ms", 0)

                    hidden_params = getattr(completion_response, "_hidden_params", None)
                    if hidden_params is not None:
                        custom_llm_provider = hidden_params.get(
                            "custom_llm_provider", custom_llm_provider or None
                        )
                        region_name = hidden_params.get("region_name", region_name)

                        # For Gemini/Vertex AI responses, trafficType is stored in
                        # provider_specific_fields.  Map it to the service_tier used
                        # by the cost key lookup (_priority / _flex suffixes) so that
                        # ON_DEMAND_PRIORITY requests are billed at priority prices.
                        if service_tier is None:
                            provider_specific = (
                                hidden_params.get("provider_specific_fields") or {}
                            )
                            raw_traffic_type = provider_specific.get("traffic_type")
                            if raw_traffic_type:
                                service_tier = _map_traffic_type_to_service_tier(
                                    raw_traffic_type
                                )
                else:
                    if model is None:
                        raise ValueError(
                            f"Model is None and does not exist in passed completion_response. Passed completion_response={completion_response}, model={model}"
                        )
                    if len(messages) > 0:
                        prompt_tokens = token_counter(model=model, messages=messages)
                    elif len(prompt) > 0:
                        prompt_tokens = token_counter(model=model, text=prompt)
                    completion_tokens = token_counter(model=model, text=completion)

                # Handle A2A calls before model check - A2A doesn't require a model
                if call_type in _A2A_CALL_TYPES:
                    from litellm.a2a_protocol.cost_calculator import A2ACostCalculator

                    return A2ACostCalculator.calculate_a2a_cost(
                        litellm_logging_obj=litellm_logging_obj
                    )

                if model is None:
                    raise ValueError(
                        f"Model is None and does not exist in passed completion_response. Passed completion_response={completion_response}, model={model}"
                    )
                if custom_llm_provider is None:
                    try:
                        model, custom_llm_provider, _, _ = litellm.get_llm_provider(
                            model=model
                        )  # strip the llm provider from the model name -> for image gen cost calculation
                    except Exception as e:
                        verbose_logger.debug(
                            "litellm.cost_calculator.py::completion_cost() - Error inferring custom_llm_provider - {}".format(
                                str(e)
                            )
                        )
                if CostCalculatorUtils._call_type_has_image_response(
                    call_type
                ) and isinstance(completion_response, ImageResponse):
                    ### IMAGE GENERATION COST CALCULATION ###
                    return CostCalculatorUtils.route_image_generation_cost_calculator(
                        model=model,
                        custom_llm_provider=custom_llm_provider,
                        completion_response=completion_response,
                        quality=quality,
                        n=n,
                        size=size,
                        optional_params=optional_params,
                        call_type=call_type,
                    )
                elif call_type in _VIDEO_CALL_TYPES:
                    ### VIDEO GENERATION COST CALCULATION ###
                    # Extract custom model_info for deployment-specific pricing
                    _video_model_info: Optional[ModelInfo] = None
                    if custom_pricing and litellm_logging_obj is not None:
                        _litellm_params = getattr(
                            litellm_logging_obj, "litellm_params", None
                        )
                        if _litellm_params is not None:
                            _metadata = _litellm_params.get("metadata", {}) or {}
                            _video_model_info = _metadata.get("model_info", None)

                    usage_obj = getattr(completion_response, "usage", None)
                    duration_seconds: Optional[float] = None
                    video_resolution: Optional[str] = None
                    if completion_response is not None and usage_obj:
                        # Handle both dict and Pydantic Usage object
                        if isinstance(usage_obj, dict):
                            duration_seconds = usage_obj.get("duration_seconds", None)
                            _vr = usage_obj.get("video_resolution", None)
                        else:
                            duration_seconds = getattr(
                                usage_obj, "duration_seconds", None
                            )
                            _vr = getattr(usage_obj, "video_resolution", None)
                        if _vr is not None:
                            video_resolution = str(_vr).strip().lower()

                        if duration_seconds is not None:
                            # Calculate cost based on video duration using video-specific cost calculation
                            from litellm.llms.openai.cost_calculation import (
                                video_generation_cost,
                            )

                            return video_generation_cost(
                                model=model,
                                duration_seconds=duration_seconds,
                                custom_llm_provider=custom_llm_provider,
                                model_info=_video_model_info,
                                video_resolution=video_resolution,
                            )
                    # Fallback to default video cost calculation if no duration available
                    return default_video_cost_calculator(
                        model=model,
                        duration_seconds=0.0,  # Default to 0 if no duration available
                        custom_llm_provider=custom_llm_provider,
                        model_info=_video_model_info,
                        video_resolution=video_resolution,
                    )
                elif call_type in _SPEECH_CALL_TYPES:
                    prompt_characters = litellm.utils._count_characters(text=prompt)
                elif call_type in _TRANSCRIPTION_CALL_TYPES:
                    # Check _hidden_params first (duration stored there to
                    # avoid polluting the response body), then fall back to
                    # the response attribute (for verbose_json responses that
                    # naturally include duration from the provider).
                    _hidden = getattr(completion_response, "_hidden_params", {}) or {}
                    audio_transcription_file_duration = _hidden.get(
                        "audio_transcription_duration",
                        getattr(completion_response, "duration", 0.0),
                    )
                elif call_type in _RERANK_CALL_TYPES:
                    if completion_response is not None and isinstance(
                        completion_response, RerankResponse
                    ):
                        meta_obj = completion_response.meta
                        if meta_obj is not None:
                            billed_units = meta_obj.get("billed_units", {}) or {}
                        else:
                            billed_units = {}

                        rerank_billed_units = RerankBilledUnits(
                            search_units=billed_units.get("search_units"),
                            total_tokens=billed_units.get("total_tokens"),
                        )

                        search_units = (
                            billed_units.get("search_units") or 1
                        )  # cohere charges per request by default.
                        completion_tokens = search_units
                elif call_type in _SEARCH_CALL_TYPES:
                    from litellm.search import search_provider_cost_per_query

                    # Extract number_of_queries from optional_params or default to 1
                    number_of_queries = 1
                    if optional_params is not None:
                        # Check if query is a list (multiple queries)
                        query = optional_params.get("query")
                        if isinstance(query, list):
                            number_of_queries = len(query)
                        elif query is not None:
                            number_of_queries = 1

                    search_model = model or ""
                    if custom_llm_provider and "/" not in search_model:
                        # If model is like "tavily-search", construct "tavily/search" for cost lookup
                        search_model = f"{custom_llm_provider}/search"

                    (
                        prompt_cost,
                        completion_cost_result,
                    ) = search_provider_cost_per_query(
                        model=search_model,
                        custom_llm_provider=custom_llm_provider,
                        number_of_queries=number_of_queries,
                        optional_params=optional_params,
                    )

                    # Return the total cost (prompt_cost + completion_cost, but for search it's just prompt_cost)
                    _final_cost = prompt_cost + completion_cost_result

                    # Apply discount
                    original_cost = _final_cost
                    (
                        _final_cost,
                        discount_percent,
                        discount_amount,
                    ) = _apply_cost_discount(
                        base_cost=_final_cost,
                        custom_llm_provider=custom_llm_provider,
                    )

                    # Apply margin from module-level config if configured
                    (
                        _final_cost,
                        margin_percent,
                        margin_fixed_amount,
                        margin_total_amount,
                    ) = _apply_cost_margin(
                        base_cost=_final_cost,
                        custom_llm_provider=custom_llm_provider,
                    )

                    # Store cost breakdown in logging object if available
                    _store_cost_breakdown_in_logging_obj(
                        litellm_logging_obj=litellm_logging_obj,
                        prompt_tokens_cost_usd_dollar=prompt_cost,
                        completion_tokens_cost_usd_dollar=completion_cost_result,
                        cost_for_built_in_tools_cost_usd_dollar=0.0,
                        total_cost_usd_dollar=_final_cost,
                        original_cost=original_cost,
                        discount_percent=discount_percent,
                        discount_amount=discount_amount,
                        margin_percent=margin_percent,
                        margin_fixed_amount=margin_fixed_amount,
                        margin_total_amount=margin_total_amount,
                    )

                    return _final_cost
                elif call_type == _AREALTIME_CALL_TYPE and isinstance(
                    completion_response, LiteLLMRealtimeStreamLoggingObject
                ):
                    if (
                        cost_per_token_usage_object is None
                        or custom_llm_provider is None
                    ):
                        raise ValueError(
                            "usage object and custom_llm_provider must be provided for realtime stream cost calculation. Got cost_per_token_usage_object={}, custom_llm_provider={}".format(
                                cost_per_token_usage_object,
                                custom_llm_provider,
                            )
                        )
                    return handle_realtime_stream_cost_calculation(
                        results=completion_response.results,
                        combined_usage_object=cost_per_token_usage_object,
                        custom_llm_provider=custom_llm_provider,
                        litellm_model_name=model,
                        data_residency=data_residency,
                    )
                elif call_type == _MCP_CALL_TYPE:
                    from litellm.proxy._experimental.mcp_server.cost_calculator import (
                        MCPCostCalculator,
                    )

                    return MCPCostCalculator.calculate_mcp_tool_call_cost(
                        litellm_logging_obj=litellm_logging_obj
                    )
                # Calculate cost based on prompt_tokens, completion_tokens
                if (
                    "togethercomputer" in model
                    or "together_ai" in model
                    or custom_llm_provider == "together_ai"
                ):
                    # together ai prices based on size of llm
                    # get_model_params_and_category takes a model name and returns the category of LLM size it is in model_prices_and_context_window.json

                    model = get_model_params_and_category(
                        model, call_type=CallTypes(call_type)
                    )

                # replicate llms are calculate based on time for request running
                # see https://replicate.com/pricing
                elif (
                    model in litellm.replicate_models or "replicate" in model
                ) and model not in litellm.model_cost:
                    # for unmapped replicate model, default to replicate's time tracking logic
                    return get_replicate_completion_pricing(completion_response, total_time)  # type: ignore

                if model is None:
                    raise ValueError(
                        f"Model is None and does not exist in passed completion_response. Passed completion_response={completion_response}, model={model}"
                    )

                if (
                    custom_llm_provider is not None
                    and custom_llm_provider == "vertex_ai"
                ):
                    # Calculate the prompt characters + response characters
                    if len(messages) > 0:
                        prompt_string = litellm.utils.get_formatted_prompt(
                            data={"messages": messages}, call_type="completion"
                        )

                        prompt_characters = litellm.utils._count_characters(
                            text=prompt_string
                        )
                    if completion_response is not None and isinstance(
                        completion_response, ModelResponse
                    ):
                        completion_string = litellm.utils.get_response_string(
                            response_obj=completion_response
                        )
                        completion_characters = litellm.utils._count_characters(
                            text=completion_string
                        )

                # Get the original request model for router detection
                request_model_for_cost = None
                if litellm_logging_obj is not None:
                    request_model_for_cost = litellm_logging_obj.model

                (
                    prompt_tokens_cost_usd_dollar,
                    completion_tokens_cost_usd_dollar,
                ) = cost_per_token(
                    model=model,
                    prompt_tokens=prompt_tokens or 0,
                    completion_tokens=completion_tokens or 0,
                    custom_llm_provider=custom_llm_provider,
                    response_time_ms=total_time,
                    region_name=region_name,
                    custom_cost_per_second=custom_cost_per_second,
                    custom_cost_per_token=custom_cost_per_token,
                    prompt_characters=prompt_characters,
                    completion_characters=completion_characters,
                    cache_creation_input_tokens=cache_creation_input_tokens,
                    cache_read_input_tokens=cache_read_input_tokens,
                    usage_object=cost_per_token_usage_object,
                    call_type=call_type,
                    audio_transcription_file_duration=audio_transcription_file_duration,
                    rerank_billed_units=rerank_billed_units,
                    service_tier=service_tier,
                    data_residency=data_residency,
                    response=completion_response,
                    request_model=request_model_for_cost,
                )

                # Get additional costs from provider (e.g., routing fees, infrastructure costs)
                if custom_llm_provider == "azure_ai":
                    model_for_additional_costs = request_model_for_cost
                    if completion_response is not None:
                        hidden_params = (
                            getattr(completion_response, "_hidden_params", None) or {}
                        )
                        hidden_model = hidden_params.get("model") or hidden_params.get(
                            "litellm_model_name"
                        )
                        if hidden_model and (
                            "model_router" in (hidden_model or "").lower()
                            or "model-router" in (hidden_model or "").lower()
                        ):
                            model_for_additional_costs = hidden_model
                        elif model_for_additional_costs is None:
                            model_for_additional_costs = hidden_model
                    if model_for_additional_costs is None:
                        model_for_additional_costs = model
                    additional_costs = _get_additional_costs(
                        model=model_for_additional_costs,
                        custom_llm_provider=custom_llm_provider,
                        prompt_tokens=prompt_tokens or 0,
                        completion_tokens=completion_tokens or 0,
                    )
                else:
                    additional_costs = None

                _final_cost = (
                    prompt_tokens_cost_usd_dollar + completion_tokens_cost_usd_dollar
                )
                cost_for_built_in_tools = (
                    StandardBuiltInToolCostTracking.get_cost_for_built_in_tools(
                        model=model,
                        response_object=completion_response,
                        usage=cost_per_token_usage_object,
                        standard_built_in_tools_params=standard_built_in_tools_params,
                        custom_llm_provider=custom_llm_provider,
                    )
                )
                _final_cost += cost_for_built_in_tools
                if additional_costs:
                    _final_cost += sum(additional_costs.values())

                original_cost = _final_cost
                if litellm.cost_discount_config:
                    (
                        _final_cost,
                        discount_percent,
                        discount_amount,
                    ) = _apply_cost_discount(
                        base_cost=_final_cost,
                        custom_llm_provider=custom_llm_provider,
                    )
                else:
                    discount_percent = 0.0
                    discount_amount = 0.0

                # Apply margin from module-level config if configured
                if litellm.cost_margin_config:
                    (
                        _final_cost,
                        margin_percent,
                        margin_fixed_amount,
                        margin_total_amount,
                    ) = _apply_cost_margin(
                        base_cost=_final_cost,
                        custom_llm_provider=custom_llm_provider,
                    )
                else:
                    margin_percent = 0.0
                    margin_fixed_amount = 0.0
                    margin_total_amount = 0.0

                # Store cost breakdown in logging object if available
                if litellm_logging_obj is not None:
                    _cache_read_cost: Optional[float] = None
                    _cache_creation_cost: Optional[float] = None
                    if cost_per_token_usage_object is not None:
                        _cr = getattr(
                            cost_per_token_usage_object, "cache_read_input_tokens", None
                        ) or (cost_per_token_usage_object.model_extra or {}).get(
                            "cache_read_input_tokens"
                        )
                        _cc = getattr(
                            cost_per_token_usage_object,
                            "cache_creation_input_tokens",
                            None,
                        ) or (cost_per_token_usage_object.model_extra or {}).get(
                            "cache_creation_input_tokens"
                        )
                        if (_cr or _cc) and model:
                            try:
                                _mi = litellm.get_model_info(
                                    model=model, custom_llm_provider=custom_llm_provider
                                )
                                _cr_rate = _mi.get("cache_read_input_token_cost")
                                if _cr and _cr_rate is not None:
                                    _cache_read_cost = float(_cr) * float(_cr_rate)
                                _cc_rate = _mi.get("cache_creation_input_token_cost")
                                if _cc and _cc_rate is not None:
                                    _cache_creation_cost = float(_cc) * float(_cc_rate)
                            except Exception:
                                pass
                    _store_cost_breakdown_in_logging_obj(
                        litellm_logging_obj=litellm_logging_obj,
                        prompt_tokens_cost_usd_dollar=prompt_tokens_cost_usd_dollar,
                        completion_tokens_cost_usd_dollar=completion_tokens_cost_usd_dollar,
                        cost_for_built_in_tools_cost_usd_dollar=cost_for_built_in_tools,
                        total_cost_usd_dollar=_final_cost,
                        original_cost=original_cost,
                        additional_costs=additional_costs,
                        discount_percent=discount_percent,
                        discount_amount=discount_amount,
                        margin_percent=margin_percent,
                        margin_fixed_amount=margin_fixed_amount,
                        margin_total_amount=margin_total_amount,
                        cache_read_cost=_cache_read_cost,
                        cache_creation_cost=_cache_creation_cost,
                    )

                return _final_cost
            except Exception as e:
                verbose_logger.debug(
                    "litellm.cost_calculator.py::completion_cost() - Error calculating cost for model={} - {}".format(
                        model, str(e)
                    )
                )
                if idx == len(potential_model_names) - 1:
                    raise e
        raise Exception(
            "Unable to calculat cost for received potential model names - {}".format(
                potential_model_names
            )
        )
    except Exception as e:
        raise e

