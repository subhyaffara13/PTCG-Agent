
def _transform_request_body(
    messages: List[AllMessageValues],
    model: str,
    optional_params: dict,
    custom_llm_provider: Literal["vertex_ai", "vertex_ai_beta", "gemini"],
    litellm_params: dict,
    cached_content: Optional[str],
) -> RequestBody:
    """
    Common transformation logic across sync + async Gemini /generateContent calls.
    """
    # Separate system prompt from rest of message
    supports_system_message = get_supports_system_message(
        model=model, custom_llm_provider=custom_llm_provider
    )
    system_instructions, messages = _transform_system_message(
        supports_system_message=supports_system_message, messages=messages
    )
    # Checks for 'response_schema' support - if passed in
    if "response_schema" in optional_params:
        supports_response_schema = get_supports_response_schema(
            model=model, custom_llm_provider=custom_llm_provider
        )
        if supports_response_schema is False:
            user_response_schema_message = response_schema_prompt(
                model=model, response_schema=optional_params.get("response_schema")  # type: ignore
            )
            messages.append({"role": "user", "content": user_response_schema_message})
            optional_params.pop("response_schema")

    # Check for any 'litellm_param_*' set during optional param mapping

    remove_keys = []
    for k, v in optional_params.items():
        if k.startswith("litellm_param_"):
            litellm_params.update({k: v})
            remove_keys.append(k)

    optional_params = {k: v for k, v in optional_params.items() if k not in remove_keys}

    try:
        if custom_llm_provider == "gemini":
            content = litellm.GoogleAIStudioGeminiConfig()._transform_messages(
                messages=messages, model=model, litellm_params=litellm_params
            )
        else:
            content = litellm.VertexGeminiConfig()._transform_messages(
                messages=messages, model=model, litellm_params=litellm_params
            )
        tools: Optional[Tools] = optional_params.pop("tools", None)
        tool_choice: Optional[ToolConfig] = optional_params.pop("tool_choice", None)
        include_server_side_tool_invocations: bool = optional_params.pop(
            "include_server_side_tool_invocations", False
        )
        safety_settings: Optional[List[SafetSettingsConfig]] = optional_params.pop(
            "safety_settings", None
        )  # type: ignore
        # Drop output_config as it's not supported by Vertex AI
        optional_params.pop("output_config", None)
        config_fields = GenerationConfig.__annotations__.keys()

        # labels: optional explicit param and/or metadata.requester_metadata (OpenAI metadata)
        labels = pop_vertex_request_labels(optional_params, litellm_params)

        filtered_params = {
            k: v
            for k, v in optional_params.items()
            if _get_equivalent_key(k, set(config_fields))
        }

        generation_config: Optional[GenerationConfig] = GenerationConfig(
            **filtered_params
        )

        # For Gemini 2.x models, also add media_resolution to generation_config (global)
        # as a fallback, since some 2.x versions may not support per-part media_resolution.
        # Gemini 1.x does not support mediaResolution at all.
        if "gemini-2" in model:
            max_media_resolution = _extract_max_media_resolution_from_messages(messages)
            if max_media_resolution:
                media_resolution_value = _convert_detail_to_media_resolution_enum(
                    max_media_resolution
                )
                if media_resolution_value and generation_config is not None:
                    generation_config["mediaResolution"] = media_resolution_value[
                        "level"
                    ]

        data = RequestBody(contents=content)
        # Vertex rejects system_instruction/tools/toolConfig alongside cachedContent.
        # Treat dropping these fields as a request mutation guarded by modify_params.
        can_send_cache_incompatible_fields = (
            cached_content is None or litellm.modify_params is False
        )
        if can_send_cache_incompatible_fields:
            if system_instructions is not None:
                data["system_instruction"] = system_instructions
            if tools is not None:
                data["tools"] = tools
            if tool_choice is not None:
                data["toolConfig"] = tool_choice
            if include_server_side_tool_invocations:
                if "toolConfig" not in data:
                    data["toolConfig"] = {}
                data["toolConfig"]["includeServerSideToolInvocations"] = True
        if safety_settings is not None:
            data["safetySettings"] = safety_settings
        if generation_config is not None and len(generation_config) > 0:
            data["generationConfig"] = generation_config
        if cached_content is not None:
            data["cachedContent"] = cached_content

        if service_tier := optional_params.pop("service_tier", None):
            if isinstance(service_tier, str):
                if service_tier.lower() == "default":
                    data["serviceTier"] = "standard"
                else:
                    data["serviceTier"] = service_tier.lower()
            else:
                data["serviceTier"] = service_tier

        # Only add labels for Vertex AI endpoints (not Google GenAI/AI Studio) and only if non-empty
        if labels and custom_llm_provider != LlmProviders.GEMINI:
            data["labels"] = labels
        _pop_and_merge_extra_body(data, optional_params)
        _rewrite_google_maps_response_format(data)
    except Exception as e:
        raise e

    return data

