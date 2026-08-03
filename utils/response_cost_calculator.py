from typing import Optional, Union

def response_cost_calculator(
    response_object: Union[
        ModelResponse,
        EmbeddingResponse,
        ImageResponse,
        TranscriptionResponse,
        TextCompletionResponse,
        HttpxBinaryResponseContent,
        RerankResponse,
        ResponsesAPIResponse,
        LiteLLMRealtimeStreamLoggingObject,
        OpenAIModerationResponse,
        Response,
        SearchResponse,
    ],
    model: str,
    custom_llm_provider: Optional[str],
    call_type: Literal[
        "embedding",
        "aembedding",
        "completion",
        "acompletion",
        "atext_completion",
        "text_completion",
        "image_generation",
        "aimage_generation",
        "moderation",
        "amoderation",
        "atranscription",
        "transcription",
        "aspeech",
        "speech",
        "rerank",
        "arerank",
        "search",
        "asearch",
    ],
    optional_params: dict,
    cache_hit: Optional[bool] = None,
    base_model: Optional[str] = None,
    custom_pricing: Optional[bool] = None,
    prompt: str = "",
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
    Returns
    - float or None: cost of response
    """
    try:
        response_cost: float = 0.0
        if cache_hit is not None and cache_hit is True:
            response_cost = 0.0
        else:
            if isinstance(response_object, BaseModel):
                if hasattr(response_object, "_hidden_params"):
                    response_object._hidden_params["optional_params"] = optional_params
                    provider_response_cost = get_response_cost_from_hidden_params(
                        response_object._hidden_params
                    )
                    if provider_response_cost is not None:
                        return provider_response_cost

            response_cost = completion_cost(
                completion_response=response_object,
                model=model,
                call_type=call_type,
                custom_llm_provider=custom_llm_provider,
                optional_params=optional_params,
                custom_pricing=custom_pricing,
                base_model=base_model,
                prompt=prompt,
                standard_built_in_tools_params=standard_built_in_tools_params,
                litellm_model_name=litellm_model_name,
                router_model_id=router_model_id,
                litellm_logging_obj=litellm_logging_obj,
                service_tier=service_tier,
                data_residency=data_residency,
            )
        return response_cost
    except Exception as e:
        raise e

