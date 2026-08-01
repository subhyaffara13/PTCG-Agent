
def cost_per_token(
    model: str = "",
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    response_time_ms: Optional[float] = 0.0,
    custom_llm_provider: Optional[str] = None,
    region_name=None,
    ### CHARACTER PRICING ###
    prompt_characters: Optional[int] = None,
    completion_characters: Optional[int] = None,
    ### PROMPT CACHING PRICING ### - used for anthropic
    cache_creation_input_tokens: Optional[int] = 0,
    cache_read_input_tokens: Optional[int] = 0,
    ### CUSTOM PRICING ###
    custom_cost_per_token: Optional[CostPerToken] = None,
    custom_cost_per_second: Optional[float] = None,
    ### NUMBER OF QUERIES ###
    number_of_queries: Optional[int] = None,
    ### USAGE OBJECT ###
    usage_object: Optional[Usage] = None,  # just read the usage object if provided
    ### BILLED UNITS ###
    rerank_billed_units: Optional[RerankBilledUnits] = None,
    ### CALL TYPE ###
    call_type: CallTypesLiteral = "completion",
    audio_transcription_file_duration: float = 0.0,  # for audio transcription calls - the file time in seconds
    ### SERVICE TIER ###
    service_tier: Optional[str] = None,  # for OpenAI service tier pricing
    ### DATA RESIDENCY ###
    data_residency: Optional[
        str
    ] = None,  # for OpenAI regional-processing uplift (e.g. "eu", "us")
    response: Optional[Any] = None,
    ### REQUEST MODEL ###
    request_model: Optional[str] = None,  # original request model for router detection
) -> Tuple[float, float]:  # type: ignore
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Parameters:
        model (str): The name of the model to use. Default is ""
        prompt_tokens (int): The number of tokens in the prompt.
        completion_tokens (int): The number of tokens in the completion.
        response_time (float): The amount of time, in milliseconds, it took the call to complete.
        prompt_characters (float): The number of characters in the prompt. Used for vertex ai cost calculation.
        completion_characters (float): The number of characters in the completion response. Used for vertex ai cost calculation.
        custom_llm_provider (str): The llm provider to whom the call was made (see init.py for full list)
        custom_cost_per_token: Optional[CostPerToken]: the cost per input + output token for the llm api call.
        custom_cost_per_second: Optional[float]: the cost per second for the llm api call.
        call_type: Optional[str]: the call type

    Returns:
        tuple: A tuple containing the cost in USD dollars for prompt tokens and completion tokens, respectively.
    """

    if model is None:
        raise Exception("Invalid arg. Model cannot be none.")

    ## RECONSTRUCT USAGE BLOCK ##
    if usage_object is not None:
        usage_block = usage_object
    else:
        usage_block = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            cache_creation_input_tokens=cache_creation_input_tokens,
            cache_read_input_tokens=cache_read_input_tokens,
        )

    ## CUSTOM PRICING ##
    # Normalize cache token counts across providers:
    #   - OpenAI-compatible: usage.prompt_tokens_details.cached_tokens
    #     (prompt_tokens already INCLUDES cached_tokens)
    #   - Anthropic: usage.cache_read_input_tokens / cache_creation_input_tokens
    #     (prompt_tokens does NOT include these — adjust before calling helper)
    _cache_read_tokens: float = 0
    _cache_creation_tokens: float = 0
    _is_anthropic_style = False

    if usage_object is not None:
        _pt_details = getattr(usage_object, "prompt_tokens_details", None)
        if _pt_details is not None:
            _cache_read_tokens = float(getattr(_pt_details, "cached_tokens", 0) or 0)
            # OpenAI-compatible providers report cache-write tokens under
            # either `cache_write_tokens` (kimi-k2) or `cache_creation_tokens`.
            # Mirror db_spend_update_writer to stay symmetric.
            _cache_creation_tokens = float(
                getattr(_pt_details, "cache_write_tokens", 0)
                or getattr(_pt_details, "cache_creation_tokens", 0)
                or 0
            )

        _anthropic_read = getattr(usage_object, "cache_read_input_tokens", None)
        _anthropic_create = getattr(usage_object, "cache_creation_input_tokens", None)
        if _anthropic_read is not None or _anthropic_create is not None:
            _is_anthropic_style = True
            if _anthropic_read is not None:
                _cache_read_tokens = float(_anthropic_read)
            if _anthropic_create is not None:
                _cache_creation_tokens = float(_anthropic_create)

    if not _cache_read_tokens and cache_read_input_tokens:
        _cache_read_tokens = float(cache_read_input_tokens)
        _is_anthropic_style = True
    if not _cache_creation_tokens and cache_creation_input_tokens:
        _cache_creation_tokens = float(cache_creation_input_tokens)
        _is_anthropic_style = True

    # Anthropic reports prompt_tokens as input_tokens (excluding cache tokens).
    # Adjust so the helper's "prompt_tokens includes cache tokens" invariant holds.
    _normalized_prompt_tokens = float(prompt_tokens)
    if _is_anthropic_style:
        _normalized_prompt_tokens += _cache_read_tokens + _cache_creation_tokens

    response_cost = _cost_per_token_custom_pricing_helper(
        prompt_tokens=_normalized_prompt_tokens,
        completion_tokens=completion_tokens,
        response_time_ms=response_time_ms,
        cached_tokens=_cache_read_tokens,
        cache_creation_tokens=_cache_creation_tokens,
        custom_cost_per_second=custom_cost_per_second,
        custom_cost_per_token=custom_cost_per_token,
    )

    if response_cost is not None:
        return response_cost[0], response_cost[1]

    # given
    prompt_tokens_cost_usd_dollar: float = 0
    completion_tokens_cost_usd_dollar: float = 0
    model_cost_ref = litellm.model_cost
    # Only callers that explicitly pass `custom_llm_provider` get the
    # dedup/prefix-join treatment. When provider is omitted, preserve legacy
    # behavior: `model_with_provider` stays equal to the raw `model` string
    # (provider is detected below for downstream use only).
    caller_supplied_provider = custom_llm_provider is not None

    # `model` is normally a string, but callers that mock the transport can pass
    # non-string objects. Only run the string-based dedup/prefix-join when it is
    # actually a string — e.g. a MagicMock's `.startswith()` is always truthy and
    # its slices return new mocks, which would spin the dedup loop forever.
    model_is_str = isinstance(model, str)

    # Router/proxy deployments may repeat the provider segment (e.g. model_name
    # "openai/openai/gpt-5.5"). Strip duplicated `{provider}/` chains before joining.
    if caller_supplied_provider and model_is_str:
        _dup_prefix = f"{custom_llm_provider}/"
        while model.startswith(_dup_prefix):
            _remainder = model[len(_dup_prefix) :]
            if _remainder.startswith(_dup_prefix):
                model = _remainder
            else:
                break

    model_with_provider = model
    if caller_supplied_provider:
        _prov_prefix = f"{custom_llm_provider}/"
        if model_is_str and model.startswith(_prov_prefix):
            model_with_provider = model
        else:
            model_with_provider = f"{custom_llm_provider}/{model}"
        if region_name is not None:
            model_with_provider_and_region = (
                f"{custom_llm_provider}/{region_name}/{model}"
            )
            if (
                model_with_provider_and_region in model_cost_ref
            ):  # use region based pricing, if it's available
                model_with_provider = model_with_provider_and_region
    else:
        _, custom_llm_provider, _, _ = litellm.get_llm_provider(model=model)

    assert custom_llm_provider is not None  # caller-supplied or get_llm_provider

    model_without_prefix = model
    model_parts = model.split("/", 1)
    if len(model_parts) > 1:
        model_without_prefix = model_parts[1]
    else:
        model_without_prefix = model
    """
    Code block that formats model to lookup in litellm.model_cost
    Option1. model = "bedrock/ap-northeast-1/anthropic.claude-instant-v1". This is the most accurate since it is region based. Should always be option 1
    Option2. model = "openai/gpt-4"       - model = provider/model
    Option3. model = "anthropic.claude-3" - model = model
    """
    if (
        model_with_provider in model_cost_ref
    ):  # Option 2. use model with provider, model = "openai/gpt-4"
        model = model_with_provider
    elif model in model_cost_ref:  # Option 1. use model passed, model="gpt-4"
        model = model
    elif (
        model_without_prefix in model_cost_ref
    ):  # Option 3. if user passed model="bedrock/anthropic.claude-3", use model="anthropic.claude-3"
        model = model_without_prefix

    # see this https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
    if call_type == "speech" or call_type == "aspeech":
        speech_model_info = litellm.get_model_info(
            model=model_without_prefix, custom_llm_provider=custom_llm_provider
        )
        cost_metric = select_cost_metric_for_model(speech_model_info)
        prompt_cost: float = 0.0
        completion_cost: float = 0.0
        if cost_metric == "cost_per_character":
            if prompt_characters is None:
                raise ValueError(
                    "prompt_characters must be provided for tts calls. prompt_characters={}, model={}, custom_llm_provider={}, call_type={}".format(
                        prompt_characters,
                        model,
                        custom_llm_provider,
                        call_type,
                    )
                )
            _prompt_cost, _completion_cost = _generic_cost_per_character(
                model=model_without_prefix,
                custom_llm_provider=custom_llm_provider,
                prompt_characters=prompt_characters,
                completion_characters=0,
                custom_prompt_cost=None,
                custom_completion_cost=0,
            )
            if _prompt_cost is None or _completion_cost is None:
                raise ValueError(
                    "cost for tts call is None. prompt_cost={}, completion_cost={}, model={}, custom_llm_provider={}, prompt_characters={}, completion_characters={}".format(
                        _prompt_cost,
                        _completion_cost,
                        model_without_prefix,
                        custom_llm_provider,
                        prompt_characters,
                        completion_characters,
                    )
                )
            prompt_cost = _prompt_cost
            completion_cost = _completion_cost
        elif cost_metric == "cost_per_token":
            prompt_cost, completion_cost = generic_cost_per_token(
                model=model_without_prefix,
                usage=usage_block,
                custom_llm_provider=custom_llm_provider,
                service_tier=service_tier,
                data_residency=data_residency,
            )

        return prompt_cost, completion_cost
    elif call_type == "arerank" or call_type == "rerank":
        return rerank_cost(
            model=model,
            custom_llm_provider=custom_llm_provider,
            billed_units=rerank_billed_units,
        )
    elif call_type == "avector_store_search" or call_type == "vector_store_search":
        return vector_store_search_cost(
            model=model,
            custom_llm_provider=custom_llm_provider,
            response=cast(VectorStoreSearchResponse, response),
        )
    elif call_type == "ocr" or call_type == "aocr":
        return ocr_cost(
            model=model,
            custom_llm_provider=custom_llm_provider,
            response=response,
        )
    elif (
        call_type == "aretrieve_batch"
        or call_type == "retrieve_batch"
        or call_type == CallTypes.aretrieve_batch
        or call_type == CallTypes.retrieve_batch
    ):
        return batch_cost_calculator(
            usage=usage_block,
            model=model,
            custom_llm_provider=custom_llm_provider,
            data_residency=data_residency,
        )
    elif call_type == "atranscription" or call_type == "transcription":
        if _transcription_usage_has_token_details(usage_block):
            return openai_cost_per_token(
                model=model_without_prefix,
                usage=usage_block,
                service_tier=service_tier,
                data_residency=data_residency,
            )

        return openai_cost_per_second(
            model=model_without_prefix,
            custom_llm_provider=custom_llm_provider,
            duration=audio_transcription_file_duration,
        )
    elif call_type == "search" or call_type == "asearch":
        # Search providers use per-query pricing
        from litellm.search import search_provider_cost_per_query

        return search_provider_cost_per_query(
            model=model,
            custom_llm_provider=custom_llm_provider,
            number_of_queries=number_of_queries or 1,
            optional_params=(
                response._hidden_params
                if response and hasattr(response, "_hidden_params")
                else None
            ),
        )
    elif custom_llm_provider == "vertex_ai":
        cost_router = google_cost_router(
            model=model_without_prefix,
            custom_llm_provider=custom_llm_provider,
            call_type=call_type,
        )
        if cost_router == "cost_per_character":
            return google_cost_per_character(
                model=model_without_prefix,
                custom_llm_provider=custom_llm_provider,
                prompt_characters=prompt_characters,
                completion_characters=completion_characters,
                usage=usage_block,
            )
        elif cost_router == "cost_per_token":
            return google_cost_per_token(
                model=model_without_prefix,
                custom_llm_provider=custom_llm_provider,
                usage=usage_block,
                service_tier=service_tier,
            )
    elif custom_llm_provider == "anthropic":
        return anthropic_cost_per_token(
            model=model, usage=usage_block, service_tier=service_tier
        )
    elif custom_llm_provider == "bedrock":
        return bedrock_cost_per_token(
            model=model, usage=usage_block, service_tier=service_tier
        )
    elif custom_llm_provider == "openai":
        return openai_cost_per_token(
            model=model,
            usage=usage_block,
            service_tier=service_tier,
            data_residency=data_residency,
        )
    elif custom_llm_provider == "databricks":
        return databricks_cost_per_token(model=model, usage=usage_block)
    elif custom_llm_provider == "fireworks_ai":
        return fireworks_ai_cost_per_token(model=model, usage=usage_block)
    elif custom_llm_provider == "azure":
        return azure_openai_cost_per_token(
            model=model,
            usage=usage_block,
            response_time_ms=response_time_ms,
            service_tier=service_tier,
        )
    elif custom_llm_provider == "gemini":
        return gemini_cost_per_token(
            model=model, usage=usage_block, service_tier=service_tier
        )
    elif custom_llm_provider == "deepseek":
        return deepseek_cost_per_token(model=model, usage=usage_block)
    elif custom_llm_provider == "perplexity":
        return perplexity_cost_per_token(model=model, usage=usage_block)
    elif custom_llm_provider == "xai":
        return xai_cost_per_token(model=model, usage=usage_block)
    elif custom_llm_provider == "lemonade":
        return lemonade_cost_per_token(model=model, usage=usage_block)
    elif custom_llm_provider == "dashscope":
        from litellm.llms.dashscope.cost_calculator import (
            cost_per_token as dashscope_cost_per_token,
        )

        return dashscope_cost_per_token(model=model, usage=usage_block)
    elif custom_llm_provider == "azure_ai":
        return azure_ai_cost_per_token(
            model=model,
            usage=usage_block,
            response_time_ms=response_time_ms,
            request_model=request_model,
            service_tier=service_tier,
        )
    else:
        model_info = _cached_get_model_info_helper(
            model=model, custom_llm_provider=custom_llm_provider
        )

        if (model_info.get("input_cost_per_token") or 0.0) > 0 or (
            model_info.get("output_cost_per_token") or 0.0
        ) > 0:
            return generic_cost_per_token(
                model=model,
                usage=usage_block,
                custom_llm_provider=custom_llm_provider,
                service_tier=service_tier,
                data_residency=data_residency,
            )

        if (
            model_info.get("input_cost_per_second", None) is not None
            and response_time_ms is not None
        ):
            verbose_logger.debug(
                "For model=%s - input_cost_per_second: %s; response time: %s",
                model,
                model_info.get("input_cost_per_second", None),
                response_time_ms,
            )
            ## COST PER SECOND ##
            prompt_tokens_cost_usd_dollar = (
                model_info["input_cost_per_second"] * response_time_ms / 1000  # type: ignore
            )

        if (
            model_info.get("output_cost_per_second", None) is not None
            and response_time_ms is not None
        ):
            verbose_logger.debug(
                "For model=%s - output_cost_per_second: %s; response time: %s",
                model,
                model_info.get("output_cost_per_second", None),
                response_time_ms,
            )
            ## COST PER SECOND ##
            completion_tokens_cost_usd_dollar = (
                model_info["output_cost_per_second"] * response_time_ms / 1000  # type: ignore
            )

        verbose_logger.debug(
            "Returned custom cost for model=%s - prompt_tokens_cost_usd_dollar: %s, completion_tokens_cost_usd_dollar: %s",
            model,
            prompt_tokens_cost_usd_dollar,
            completion_tokens_cost_usd_dollar,
        )
        return prompt_tokens_cost_usd_dollar, completion_tokens_cost_usd_dollar


def cost_per_token(model: str, usage: "Usage") -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.
    Follows the same logic as Anthropic's cost per token calculation.
    """
    return generic_cost_per_token(
        model=model, usage=usage, custom_llm_provider="amazon_nova"
    )


def cost_per_token(
    model: str, usage: "Usage", service_tier: str | None = None
) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Input:
        - model: str, the model name without provider prefix
        - usage: LiteLLM Usage block, containing anthropic caching information
        - service_tier: the service tier the request was served at (e.g. "priority"),
          read from the Anthropic response usage and used to select tier-specific pricing

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd
    """
    prompt_cost, completion_cost = generic_cost_per_token(
        model=model,
        usage=usage,
        custom_llm_provider="anthropic",
        service_tier=service_tier,
    )

    # Apply provider_specific_entry multipliers for geo/speed routing
    try:
        model_info = litellm.get_model_info(
            model=model, custom_llm_provider="anthropic"
        )
        provider_specific_entry: dict = model_info.get("provider_specific_entry") or {}

        multiplier = 1.0
        if (
            hasattr(usage, "inference_geo")
            and usage.inference_geo
            and usage.inference_geo.lower() not in ["global", "not_available"]
        ):
            multiplier *= provider_specific_entry.get(usage.inference_geo.lower(), 1.0)
        if hasattr(usage, "speed") and usage.speed == "fast":
            multiplier *= provider_specific_entry.get("fast", 1.0)

        if multiplier != 1.0:
            cache_cost = _compute_cache_only_cost(
                model_info=model_info, usage=usage, service_tier=service_tier
            )
            prompt_cost = (prompt_cost - cache_cost) * multiplier + cache_cost
            completion_cost *= multiplier
    except Exception:
        pass

    return prompt_cost, completion_cost


def cost_per_token(
    model: str,
    usage: Usage,
    response_time_ms: Optional[float] = 0.0,
    service_tier: Optional[str] = None,
) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Input:
        - model: str, the model name without provider prefix
        - usage: LiteLLM Usage block, containing caching and audio token information

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd
    """
    ## GET MODEL INFO
    model_info = get_model_info(model=model, custom_llm_provider="azure")

    ## Speech / Audio cost calculation (cost per second for TTS models)
    if (
        "output_cost_per_second" in model_info
        and model_info["output_cost_per_second"] is not None
        and response_time_ms is not None
    ):
        verbose_logger.debug(
            f"For model={model} - output_cost_per_second: {model_info.get('output_cost_per_second')}; response time: {response_time_ms}"
        )
        ## COST PER SECOND ##
        prompt_cost = 0.0
        completion_cost = model_info["output_cost_per_second"] * response_time_ms / 1000
        return prompt_cost, completion_cost

    ## Use generic cost calculator for all other cases
    ## This properly handles: text tokens, audio tokens, cached tokens, reasoning tokens, etc.
    return generic_cost_per_token(
        model=model,
        usage=usage,
        custom_llm_provider="azure",
        service_tier=service_tier,
    )


def cost_per_token(
    model: str,
    usage: Usage,
    response_time_ms: Optional[float] = 0.0,
    request_model: Optional[str] = None,
    service_tier: Optional[str] = None,
) -> Tuple[float, float]:
    """
    Calculate the cost per token for Azure AI models.

    For Azure AI Foundry Model Router:
    - Adds a flat cost of $0.14 per million input tokens (from model_prices_and_context_window.json)
    - Plus the cost of the actual model used (handled by generic_cost_per_token)

    Args:
        model: str, the model name without provider prefix (from response)
        usage: LiteLLM Usage block
        response_time_ms: Optional response time in milliseconds
        request_model: Optional[str], the original request model name (to detect router usage)

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd

    Raises:
        ValueError: If the model is not found in the cost map and cost cannot be calculated
            (except for Model Router models where we return just the routing flat cost)
    """
    prompt_cost = 0.0
    completion_cost = 0.0

    # Determine if this was a model router request
    # Check both the response model and the request model
    is_router_request = _is_azure_model_router(model) or (
        request_model is not None and _is_azure_model_router(request_model)
    )

    # Calculate base cost using generic cost calculator
    # This may raise an exception if the model is not in the cost map
    try:
        prompt_cost, completion_cost = generic_cost_per_token(
            model=model,
            usage=usage,
            custom_llm_provider="azure_ai",
            service_tier=service_tier,
        )
    except Exception as e:
        # For Model Router, the model name (e.g., "azure-model-router") may not be in the cost map
        # because it's a routing service, not an actual model. In this case, we continue
        # to calculate just the routing flat cost.
        if not _is_azure_model_router(model):
            # Re-raise for non-router models - they should have pricing defined
            raise
        verbose_logger.debug(
            f"Azure AI Model Router: model '{model}' not in cost map, calculating routing flat cost only. Error: {e}"
        )

    # Add flat cost for Azure Model Router
    # The flat cost is defined in model_prices_and_context_window.json for azure_ai/model_router
    if is_router_request:
        # Use the request model for flat cost calculation if available, otherwise use response model
        router_model_for_calc = request_model if request_model else model
        router_flat_cost = calculate_azure_model_router_flat_cost(
            router_model_for_calc, usage.prompt_tokens
        )

        if router_flat_cost > 0:
            verbose_logger.debug(
                f"Azure AI Model Router flat cost: ${router_flat_cost:.6f} "
                f"({usage.prompt_tokens} tokens × ${router_flat_cost / usage.prompt_tokens:.9f}/token)"
            )

            # Add flat cost to prompt cost
            prompt_cost += router_flat_cost

    return prompt_cost, completion_cost


def cost_per_token(
    model: str, usage: "Usage", service_tier: Optional[str] = None
) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Follows the same logic as Anthropic's cost per token calculation.
    """
    return generic_cost_per_token(
        model=model,
        usage=usage,
        custom_llm_provider="bedrock",
        service_tier=service_tier,
    )


def cost_per_token(model: str, usage: Usage) -> Tuple[float, float]:
    """
    Calculate cost per token for Dashscope models.

    Supports both tiered and flat pricing with cached and reasoning tokens.

    Args:
        model: Model name without provider prefix
        usage: LiteLLM Usage block

    Returns:
        Tuple[float, float] - (prompt_cost_in_usd, completion_cost_in_usd)
    """
    model_info = get_model_info(model=model, custom_llm_provider="dashscope")
    breakdown = _extract_token_breakdown(usage)
    tiered_pricing = (
        model_info.get("tiered_pricing")
        if isinstance(model_info.get("tiered_pricing"), list)
        else None
    )

    prompt_cost = _calculate_prompt_cost(
        breakdown=breakdown, model_info=model_info, tiered_pricing=tiered_pricing
    )
    completion_cost = _calculate_completion_cost(
        breakdown=breakdown, model_info=model_info, tiered_pricing=tiered_pricing
    )

    return prompt_cost, completion_cost


def cost_per_token(model: str, usage: Usage) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Input:
        - model: str, the model name without provider prefix
        - usage: LiteLLM Usage block, containing anthropic caching information

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd
    """
    base_model = model
    if model.startswith("databricks/dbrx-instruct") or model.startswith(
        "dbrx-instruct"
    ):
        base_model = "databricks-dbrx-instruct"
    elif model.startswith("databricks/meta-llama-3.1-70b-instruct") or model.startswith(
        "meta-llama-3.1-70b-instruct"
    ):
        base_model = "databricks-meta-llama-3-1-70b-instruct"
    elif model.startswith(
        "databricks/meta-llama-3.1-405b-instruct"
    ) or model.startswith("meta-llama-3.1-405b-instruct"):
        base_model = "databricks-meta-llama-3-1-405b-instruct"
    elif model.startswith("databricks/mixtral-8x7b-instruct-v0.1") or model.startswith(
        "mixtral-8x7b-instruct-v0.1"
    ):
        base_model = "databricks-mixtral-8x7b-instruct"
    elif model.startswith("databricks/mixtral-8x7b-instruct-v0.1") or model.startswith(
        "mixtral-8x7b-instruct-v0.1"
    ):
        base_model = "databricks-mixtral-8x7b-instruct"
    elif model.startswith("databricks/bge-large-en") or model.startswith(
        "bge-large-en"
    ):
        base_model = "databricks-bge-large-en"
    elif model.startswith("databricks/gte-large-en") or model.startswith(
        "gte-large-en"
    ):
        base_model = "databricks-gte-large-en"
    elif model.startswith("databricks/llama-2-70b-chat") or model.startswith(
        "llama-2-70b-chat"
    ):
        base_model = "databricks-llama-2-70b-chat"
    ## GET MODEL INFO
    model_info = get_model_info(model=base_model, custom_llm_provider="databricks")

    ## CALCULATE INPUT COST

    prompt_cost: float = usage["prompt_tokens"] * model_info["input_cost_per_token"]

    ## CALCULATE OUTPUT COST
    completion_cost = usage["completion_tokens"] * model_info["output_cost_per_token"]

    return prompt_cost, completion_cost


def cost_per_token(model: str, usage: Usage) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Follows the same logic as Anthropic's cost per token calculation.
    """
    return generic_cost_per_token(
        model=model, usage=usage, custom_llm_provider="deepseek"
    )


def cost_per_token(model: str, usage: Usage) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Input:
        - model: str, the model name without provider prefix
        - usage: LiteLLM Usage block, containing anthropic caching information

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd
    """
    ## check if model mapped, else use default pricing
    try:
        model_info = get_model_info(model=model, custom_llm_provider="fireworks_ai")
    except Exception:
        base_model = get_base_model_for_pricing(model_name=model)

        ## GET MODEL INFO
        model_info = get_model_info(
            model=base_model, custom_llm_provider="fireworks_ai"
        )

    ## CALCULATE INPUT COST

    prompt_cost: float = usage["prompt_tokens"] * model_info["input_cost_per_token"]

    ## CALCULATE OUTPUT COST
    completion_cost = usage["completion_tokens"] * model_info["output_cost_per_token"]

    return prompt_cost, completion_cost


def cost_per_token(
    model: str, usage: "Usage", service_tier: Optional[str] = None
) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Follows the same logic as Anthropic's cost per token calculation.
    """
    from litellm.litellm_core_utils.llm_cost_calc.utils import generic_cost_per_token

    return generic_cost_per_token(
        model=model,
        usage=usage,
        custom_llm_provider="gemini",
        service_tier=service_tier,
    )


def cost_per_token(
    model: str,
    usage: Usage,
) -> Tuple[float, float]:
    """
    Calculate cost per token for Lemonade models.

    Since Lemonade is a local/self-hosted deployment, there are no per-token costs.
    This function returns (0.0, 0.0) for all models to allow cost tracking to work
    without errors for any Lemonade model, regardless of whether it's in the
    model_prices_and_context_window.json file.

    Args:
        model: The model name (with or without "lemonade/" prefix)
        usage: Usage object containing token counts

    Returns:
        Tuple of (prompt_cost, completion_cost) - always (0.0, 0.0) for Lemonade
    """
    # Lemonade is self-hosted/local, so cost is always 0
    prompt_cost = 0.0
    completion_cost = 0.0

    return prompt_cost, completion_cost


def cost_per_token(
    model: str,
    usage: Usage,
    service_tier: Optional[str] = None,
    data_residency: Optional[str] = None,
) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Input:
        - model: str, the model name without provider prefix
        - usage: LiteLLM Usage block, containing anthropic caching information
        - data_residency: optional OpenAI data-residency region (e.g. "eu", "us"),
          inferred from api_base. Applies the model's regional-processing
          uplift multiplier when set.

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd
    """
    ## CALCULATE INPUT COST
    return generic_cost_per_token(
        model=model,
        usage=usage,
        custom_llm_provider="openai",
        service_tier=service_tier,
        data_residency=data_residency,
    )


def cost_per_token(model: str, usage: Usage) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Input:
        - model: str, the model name without provider prefix
        - usage: LiteLLM Usage block, containing perplexity-specific usage information

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd
    """
    ## USE PRE-CALCULATED COST FROM PERPLEXITY IF AVAILABLE
    ## Perplexity returns accurate cost in usage.cost.total_cost including request fees
    cost_info = getattr(usage, "cost", None)
    if cost_info is not None and isinstance(cost_info, dict):
        total_cost = cost_info.get("total_cost")
        if total_cost is not None:
            # Return total cost as completion_cost (prompt_cost=0) since Perplexity
            # doesn't break down by input/output in their cost object
            return (0.0, float(total_cost))

    ## FALLBACK: Calculate cost manually if Perplexity doesn't provide it
    ## GET MODEL INFO
    model_info = get_model_info(model=model, custom_llm_provider="perplexity")

    def _safe_float_cast(
        value: Union[str, int, float, None, object], default: float = 0.0
    ) -> float:
        """Safely cast a value to float with proper type handling for mypy."""
        if value is None:
            return default
        try:
            return float(value)  # type: ignore
        except (ValueError, TypeError):
            return default

    ## CALCULATE INPUT COST
    input_cost_per_token = _safe_float_cast(model_info.get("input_cost_per_token"))
    prompt_cost: float = (usage.prompt_tokens or 0) * input_cost_per_token

    ## ADD CITATION TOKENS COST (if present)
    citation_tokens = getattr(usage, "citation_tokens", 0) or 0
    citation_cost_value = model_info.get("citation_cost_per_token")
    if citation_tokens > 0 and citation_cost_value is not None:
        citation_cost_per_token = _safe_float_cast(citation_cost_value)
        prompt_cost += citation_tokens * citation_cost_per_token

    ## CALCULATE OUTPUT COST
    output_cost_per_token = _safe_float_cast(model_info.get("output_cost_per_token"))

    reasoning_tokens = getattr(usage, "reasoning_tokens", 0) or 0
    if (
        reasoning_tokens == 0
        and hasattr(usage, "completion_tokens_details")
        and usage.completion_tokens_details
    ):
        reasoning_tokens = (
            getattr(usage.completion_tokens_details, "reasoning_tokens", 0) or 0
        )

    reasoning_cost_value = model_info.get("output_cost_per_reasoning_token")

    # `completion_tokens` includes `reasoning_tokens` per the OpenAI/Perplexity usage
    # convention (codified for the central path in PR #18607). When a reasoning rate is
    # configured we subtract before the output-rate multiplication so the reasoning
    # tokens are not billed twice.
    if reasoning_tokens > 0 and reasoning_cost_value is not None:
        non_reasoning_completion_tokens = max(
            0, (usage.completion_tokens or 0) - reasoning_tokens
        )
        completion_cost: float = non_reasoning_completion_tokens * output_cost_per_token
        completion_cost += reasoning_tokens * _safe_float_cast(reasoning_cost_value)
    else:
        completion_cost = (usage.completion_tokens or 0) * output_cost_per_token

    ## ADD SEARCH QUERIES COST (if present)
    num_search_queries = 0
    if hasattr(usage, "prompt_tokens_details") and usage.prompt_tokens_details:
        num_search_queries = (
            getattr(usage.prompt_tokens_details, "web_search_requests", 0) or 0
        )

    # Check both possible keys for search cost (legacy and current)
    search_cost_value = model_info.get(
        "search_queries_cost_per_query"
    ) or model_info.get("search_context_cost_per_query")
    if num_search_queries > 0 and search_cost_value is not None:
        # Handle both dict and float formats
        if isinstance(search_cost_value, dict):
            # Use the "low" size as default - tests expect 0.005 / 1000
            search_cost_per_query = (
                _safe_float_cast(search_cost_value.get("search_context_size_low", 0))
                / 1000
            )
        else:
            search_cost_per_query = _safe_float_cast(search_cost_value)
        search_cost = num_search_queries * search_cost_per_query
        # Add search cost to completion cost (similar to how other providers handle it)
        completion_cost += search_cost

    return prompt_cost, completion_cost


def cost_per_token(
    model: str,
    custom_llm_provider: str,
    usage: Usage,
    service_tier: Optional[str] = None,
) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Input:
        - model: str, the model name without provider prefix
        - custom_llm_provider: str, either "vertex_ai-*" or "gemini"
        - prompt_tokens: float, the number of input tokens
        - completion_tokens: float, the number of output tokens
        - service_tier: optional tier derived from Gemini trafficType
          ("priority" for ON_DEMAND_PRIORITY, "flex" for FLEX/batch).

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd

    Raises:
        Exception if model requires >128k pricing, but model cost not mapped
    """

    ## GET MODEL INFO
    model_info = litellm.get_model_info(
        model=model, custom_llm_provider=custom_llm_provider
    )

    ## HANDLE 128k+ PRICING
    input_cost_per_token_above_128k_tokens = model_info.get(
        "input_cost_per_token_above_128k_tokens"
    )
    output_cost_per_token_above_128k_tokens = model_info.get(
        "output_cost_per_token_above_128k_tokens"
    )
    if (
        input_cost_per_token_above_128k_tokens is not None
        or output_cost_per_token_above_128k_tokens is not None
    ):
        return _handle_128k_pricing(
            model_info=model_info,
            usage=usage,
        )

    return generic_cost_per_token(
        model=model,
        custom_llm_provider=custom_llm_provider,
        usage=usage,
        service_tier=service_tier,
    )


def cost_per_token(model: str, usage: Usage) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given XAI model, prompt tokens, and completion tokens.
    Uses the generic cost calculator for all pricing logic, with XAI-specific reasoning token handling.

    Input:
        - model: str, the model name without provider prefix
        - usage: LiteLLM Usage block, containing XAI-specific usage information

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd
    """
    # XAI-specific completion cost: completion is billed as visible + reasoning
    # tokens. Detect when the transformation layer already folded them so we
    # don't double-count; fall back to raw xAI shape for callers that bypass
    # the transformation (e.g. proxy logs replayed into cost calc).
    prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
    completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
    total_tokens = int(getattr(usage, "total_tokens", 0) or 0)
    reasoning_tokens = 0
    if hasattr(usage, "completion_tokens_details") and usage.completion_tokens_details:
        reasoning_tokens = int(
            getattr(usage.completion_tokens_details, "reasoning_tokens", 0) or 0
        )

    already_normalised = total_tokens == prompt_tokens + completion_tokens
    total_completion_tokens = (
        completion_tokens
        if already_normalised
        else completion_tokens + reasoning_tokens
    )

    modified_usage = Usage(
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=total_completion_tokens,
        total_tokens=usage.total_tokens,
        prompt_tokens_details=usage.prompt_tokens_details,
        completion_tokens_details=None,
    )

    prompt_cost, completion_cost = generic_cost_per_token(
        model=model, usage=modified_usage, custom_llm_provider="xai"
    )

    return prompt_cost, completion_cost

