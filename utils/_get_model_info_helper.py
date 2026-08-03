from typing import Any, Dict, Optional

def _get_model_info_helper(
    model: str,
    custom_llm_provider: Optional[str] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ModelInfoBase:
    """
    Helper for 'get_model_info'. Separated out to avoid infinite loop caused by returning 'supported_openai_param's
    """
    try:
        azure_llms = {**litellm.azure_llms, **litellm.azure_embedding_models}
        if model in azure_llms:
            model = azure_llms[model]
        if custom_llm_provider is not None and custom_llm_provider == "vertex_ai_beta":
            custom_llm_provider = "vertex_ai"
        if custom_llm_provider is not None and custom_llm_provider == "vertex_ai":
            if "meta/" + model in litellm.vertex_llama3_models:
                model = "meta/" + model
            elif model + "@latest" in litellm.vertex_mistral_models:
                model = model + "@latest"
            elif model + "@latest" in litellm.vertex_ai_ai21_models:
                model = model + "@latest"
        ##########################
        potential_model_names = _get_potential_model_names(
            model=model, custom_llm_provider=custom_llm_provider
        )

        verbose_logger.debug(
            f"checking potential_model_names in litellm.model_cost: {potential_model_names}"
        )

        combined_model_name = potential_model_names["combined_model_name"]
        stripped_model_name = potential_model_names["stripped_model_name"]
        combined_stripped_model_name = potential_model_names[
            "combined_stripped_model_name"
        ]
        split_model = potential_model_names["split_model"]
        custom_llm_provider = potential_model_names["custom_llm_provider"]
        model_cost_custom_llm_provider = custom_llm_provider
        #########################
        provider_config: Optional[BaseLLMModelInfo] = None
        if custom_llm_provider and custom_llm_provider in LlmProvidersSet:
            provider_config = ProviderConfigManager.get_provider_model_info(
                model=model, provider=LlmProviders(custom_llm_provider)
            )
        if provider_config is not None:
            provider_get_model_info = getattr(provider_config, "get_model_info", None)
            if callable(provider_get_model_info):
                try:
                    provider_model_info = provider_get_model_info(
                        model=model,
                        api_base=api_base,
                        api_key=api_key,
                    )
                    if provider_model_info is not None:
                        return provider_model_info
                except Exception as e:
                    verbose_logger.warning(
                        "Could not get dynamic model info for model=%s, provider=%s; "
                        "falling back to the static cost map: %s",
                        model,
                        custom_llm_provider,
                        e,
                    )

        if custom_llm_provider == "huggingface":
            max_tokens = _get_max_position_embeddings(model_name=model)
            return ModelInfoBase(
                key=model,
                max_tokens=max_tokens,  # type: ignore
                max_input_tokens=None,
                max_output_tokens=None,
                input_cost_per_token=0,
                output_cost_per_token=0,
                litellm_provider="huggingface",
                mode="chat",
                supports_system_messages=None,
                supports_response_schema=None,
                supports_function_calling=None,
                supports_tool_choice=None,
                supports_assistant_prefill=None,
                supports_prompt_caching=None,
                supports_computer_use=None,
                supports_pdf_input=None,
            )
        else:
            """
            Check if: (in order of specificity)
            1. 'custom_llm_provider/model' in litellm.model_cost. Checks "groq/llama3-8b-8192" if model="llama3-8b-8192" and custom_llm_provider="groq"
            2. 'model' in litellm.model_cost. Checks "gemini-1.5-pro-002" in  litellm.model_cost if model="gemini-1.5-pro-002" and custom_llm_provider=None
            3. 'combined_stripped_model_name' in litellm.model_cost. Checks if 'gemini/gemini-1.5-flash' in model map, if 'gemini/gemini-1.5-flash-001' given.
            4. 'stripped_model_name' in litellm.model_cost. Checks if 'ft:gpt-3.5-turbo' in model map, if 'ft:gpt-3.5-turbo:my-org:custom_suffix:id' given.
            5. 'split_model' in litellm.model_cost. Checks "llama3-8b-8192" in litellm.model_cost if model="groq/llama3-8b-8192"
            """

            _model_info: Optional[Dict[str, Any]] = None
            key: Optional[str] = None

            # Use case-insensitive lookup for all model name checks
            _matched_key = _get_model_cost_key(combined_model_name)
            if _matched_key is not None:
                key = _matched_key
                _model_info = _get_model_info_from_model_cost(key=cast(str, key))
                if not _check_provider_match(
                    model_info=_model_info,
                    custom_llm_provider=model_cost_custom_llm_provider,
                ):
                    _model_info = None
            if _model_info is None:
                _matched_key = _get_model_cost_key(model)
                if _matched_key is not None:
                    key = _matched_key
                    _model_info = _get_model_info_from_model_cost(key=cast(str, key))
                    if not _check_provider_match(
                        model_info=_model_info,
                        custom_llm_provider=model_cost_custom_llm_provider,
                    ):
                        _model_info = None
            if _model_info is None:
                _matched_key = _get_model_cost_key(combined_stripped_model_name)
                if _matched_key is not None:
                    key = _matched_key
                    _model_info = _get_model_info_from_model_cost(key=cast(str, key))
                    if not _check_provider_match(
                        model_info=_model_info,
                        custom_llm_provider=model_cost_custom_llm_provider,
                    ):
                        _model_info = None
            if _model_info is None:
                _matched_key = _get_model_cost_key(stripped_model_name)
                if _matched_key is not None:
                    key = _matched_key
                    _model_info = _get_model_info_from_model_cost(key=cast(str, key))
                    if not _check_provider_match(
                        model_info=_model_info,
                        custom_llm_provider=model_cost_custom_llm_provider,
                    ):
                        _model_info = None
            if _model_info is None:
                _matched_key = _get_model_cost_key(split_model)
                if _matched_key is not None:
                    key = _matched_key
                    _model_info = _get_model_info_from_model_cost(key=cast(str, key))
                    if not _check_provider_match(
                        model_info=_model_info,
                        custom_llm_provider=model_cost_custom_llm_provider,
                    ):
                        _model_info = None

            if _model_info is None or key is None:
                raise ValueError(
                    "This model isn't mapped yet. Add it here - https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json"
                )
            _input_cost_per_token: Optional[float] = _model_info.get(
                "input_cost_per_token"
            )
            if _input_cost_per_token is None:
                # default value to 0, be noisy about this
                verbose_logger.debug(
                    "model={}, custom_llm_provider={} has no input_cost_per_token in model_cost_map. Defaulting to 0.".format(
                        model, custom_llm_provider
                    )
                )
                _input_cost_per_token = 0

            _output_cost_per_token: Optional[float] = _model_info.get(
                "output_cost_per_token"
            )
            if _output_cost_per_token is None:
                # default value to 0, be noisy about this
                verbose_logger.debug(
                    "model={}, custom_llm_provider={} has no output_cost_per_token in model_cost_map. Defaulting to 0.".format(
                        model, custom_llm_provider
                    )
                )
                _output_cost_per_token = 0

            return ModelInfoBase(
                key=key,
                max_tokens=_model_info.get("max_tokens", None),
                max_input_tokens=_model_info.get("max_input_tokens", None),
                max_output_tokens=_model_info.get("max_output_tokens", None),
                input_cost_per_token=_input_cost_per_token,
                input_cost_per_token_flex=_model_info.get(
                    "input_cost_per_token_flex", None
                ),
                input_cost_per_token_priority=_model_info.get(
                    "input_cost_per_token_priority", None
                ),
                cache_creation_input_token_cost=_model_info.get(
                    "cache_creation_input_token_cost", None
                ),
                cache_creation_input_token_cost_above_200k_tokens=_model_info.get(
                    "cache_creation_input_token_cost_above_200k_tokens", None
                ),
                cache_read_input_token_cost=_model_info.get(
                    "cache_read_input_token_cost", None
                ),
                cache_read_input_token_cost_above_200k_tokens=_model_info.get(
                    "cache_read_input_token_cost_above_200k_tokens", None
                ),
                cache_read_input_token_cost_above_200k_tokens_priority=_model_info.get(
                    "cache_read_input_token_cost_above_200k_tokens_priority", None
                ),
                cache_read_input_token_cost_above_272k_tokens=_model_info.get(
                    "cache_read_input_token_cost_above_272k_tokens", None
                ),
                cache_read_input_token_cost_above_272k_tokens_priority=_model_info.get(
                    "cache_read_input_token_cost_above_272k_tokens_priority", None
                ),
                cache_read_input_token_cost_above_512k_tokens=_model_info.get(
                    "cache_read_input_token_cost_above_512k_tokens", None
                ),
                cache_read_input_token_cost_flex=_model_info.get(
                    "cache_read_input_token_cost_flex", None
                ),
                cache_read_input_token_cost_priority=_model_info.get(
                    "cache_read_input_token_cost_priority", None
                ),
                cache_creation_input_token_cost_above_1hr=_model_info.get(
                    "cache_creation_input_token_cost_above_1hr", None
                ),
                input_cost_per_character=_model_info.get(
                    "input_cost_per_character", None
                ),
                input_cost_per_token_above_128k_tokens=_model_info.get(
                    "input_cost_per_token_above_128k_tokens", None
                ),
                input_cost_per_token_above_200k_tokens=_model_info.get(
                    "input_cost_per_token_above_200k_tokens", None
                ),
                input_cost_per_token_above_200k_tokens_priority=_model_info.get(
                    "input_cost_per_token_above_200k_tokens_priority", None
                ),
                input_cost_per_token_above_272k_tokens=_model_info.get(
                    "input_cost_per_token_above_272k_tokens", None
                ),
                input_cost_per_token_above_272k_tokens_priority=_model_info.get(
                    "input_cost_per_token_above_272k_tokens_priority", None
                ),
                input_cost_per_token_above_512k_tokens=_model_info.get(
                    "input_cost_per_token_above_512k_tokens", None
                ),
                input_cost_per_query=_model_info.get("input_cost_per_query", None),
                input_cost_per_second=_model_info.get("input_cost_per_second", None),
                input_cost_per_audio_token=_model_info.get(
                    "input_cost_per_audio_token", None
                ),
                input_cost_per_image_token=_model_info.get(
                    "input_cost_per_image_token", None
                ),
                input_cost_per_image=_model_info.get("input_cost_per_image", None),
                input_cost_per_audio_per_second=_model_info.get(
                    "input_cost_per_audio_per_second", None
                ),
                input_cost_per_video_per_second=_model_info.get(
                    "input_cost_per_video_per_second", None
                ),
                input_cost_per_token_batches=_model_info.get(
                    "input_cost_per_token_batches"
                ),
                output_cost_per_token_batches=_model_info.get(
                    "output_cost_per_token_batches"
                ),
                output_cost_per_token=_output_cost_per_token,
                output_cost_per_token_flex=_model_info.get(
                    "output_cost_per_token_flex", None
                ),
                output_cost_per_token_priority=_model_info.get(
                    "output_cost_per_token_priority", None
                ),
                regional_processing_uplift_multiplier_eu=_model_info.get(
                    "regional_processing_uplift_multiplier_eu", None
                ),
                regional_processing_uplift_multiplier_us=_model_info.get(
                    "regional_processing_uplift_multiplier_us", None
                ),
                output_cost_per_audio_token=_model_info.get(
                    "output_cost_per_audio_token", None
                ),
                output_cost_per_character=_model_info.get(
                    "output_cost_per_character", None
                ),
                output_cost_per_reasoning_token=_model_info.get(
                    "output_cost_per_reasoning_token", None
                ),
                output_cost_per_token_above_128k_tokens=_model_info.get(
                    "output_cost_per_token_above_128k_tokens", None
                ),
                output_cost_per_character_above_128k_tokens=_model_info.get(
                    "output_cost_per_character_above_128k_tokens", None
                ),
                output_cost_per_token_above_200k_tokens=_model_info.get(
                    "output_cost_per_token_above_200k_tokens", None
                ),
                output_cost_per_token_above_200k_tokens_priority=_model_info.get(
                    "output_cost_per_token_above_200k_tokens_priority", None
                ),
                output_cost_per_token_above_272k_tokens=_model_info.get(
                    "output_cost_per_token_above_272k_tokens", None
                ),
                output_cost_per_token_above_272k_tokens_priority=_model_info.get(
                    "output_cost_per_token_above_272k_tokens_priority", None
                ),
                output_cost_per_token_above_512k_tokens=_model_info.get(
                    "output_cost_per_token_above_512k_tokens", None
                ),
                output_cost_per_second=_model_info.get("output_cost_per_second", None),
                output_cost_per_second_1080p=_model_info.get(
                    "output_cost_per_second_1080p", None
                ),
                output_cost_per_video_per_second=_model_info.get(
                    "output_cost_per_video_per_second", None
                ),
                output_cost_per_image=_model_info.get("output_cost_per_image", None),
                output_cost_per_image_token=_model_info.get(
                    "output_cost_per_image_token", None
                ),
                output_vector_size=_model_info.get("output_vector_size", None),
                citation_cost_per_token=_model_info.get(
                    "citation_cost_per_token", None
                ),
                tiered_pricing=_model_info.get("tiered_pricing", None),
                litellm_provider=_model_info.get(
                    "litellm_provider", custom_llm_provider
                ),
                mode=_model_info.get("mode"),  # type: ignore
                supports_system_messages=_model_info.get(
                    "supports_system_messages", None
                ),
                supports_response_schema=_model_info.get(
                    "supports_response_schema", None
                ),
                supports_vision=_model_info.get("supports_vision", None),
                supports_function_calling=_model_info.get(
                    "supports_function_calling", None
                ),
                supports_tool_choice=_model_info.get("supports_tool_choice", None),
                supports_assistant_prefill=_model_info.get(
                    "supports_assistant_prefill", None
                ),
                supports_prompt_caching=_model_info.get(
                    "supports_prompt_caching", None
                ),
                supports_audio_input=_model_info.get("supports_audio_input", None),
                supports_audio_output=_model_info.get("supports_audio_output", None),
                supports_pdf_input=_model_info.get("supports_pdf_input", None),
                supports_embedding_image_input=_model_info.get(
                    "supports_embedding_image_input", None
                ),
                supports_native_streaming=_model_info.get(
                    "supports_native_streaming", None
                ),
                supports_native_structured_output=_model_info.get(
                    "supports_native_structured_output", None
                ),
                supports_web_search=_model_info.get("supports_web_search", None),
                supports_url_context=_model_info.get("supports_url_context", None),
                supports_reasoning=_model_info.get("supports_reasoning", None),
                supports_none_reasoning_effort=_model_info.get(
                    "supports_none_reasoning_effort", None
                ),
                supports_minimal_reasoning_effort=_model_info.get(
                    "supports_minimal_reasoning_effort", None
                ),
                supports_low_reasoning_effort=_model_info.get(
                    "supports_low_reasoning_effort", None
                ),
                supports_xhigh_reasoning_effort=_model_info.get(
                    "supports_xhigh_reasoning_effort", None
                ),
                supports_max_reasoning_effort=_model_info.get(
                    "supports_max_reasoning_effort", None
                ),
                bedrock_output_config_effort_ceiling=_model_info.get(
                    "bedrock_output_config_effort_ceiling", None
                ),
                supports_computer_use=_model_info.get("supports_computer_use", None),
                search_context_cost_per_query=_model_info.get(
                    "search_context_cost_per_query", None
                ),
                tpm=_model_info.get("tpm", None),
                rpm=_model_info.get("rpm", None),
                ocr_cost_per_page=_model_info.get("ocr_cost_per_page", None),
                ocr_cost_per_credit=_model_info.get("ocr_cost_per_credit", None),
                annotation_cost_per_page=_model_info.get(
                    "annotation_cost_per_page", None
                ),
                provider_specific_entry=_model_info.get(
                    "provider_specific_entry", None
                ),
                uses_embed_content=_model_info.get("uses_embed_content", None),
                supports_image_size=_model_info.get("supports_image_size", None),
            )
    except Exception as e:
        verbose_logger.debug(f"Error getting model info: {e}")
        raise Exception(
            "This model isn't mapped yet. model={}, custom_llm_provider={}. Add it here - https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json.".format(
                model, custom_llm_provider
            )
        )

