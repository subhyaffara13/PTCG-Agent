
def get_optional_params(
    # use the openai defaults
    # https://platform.openai.com/docs/api-reference/chat/create
    model: str,
    functions=None,
    function_call=None,
    temperature=None,
    top_p=None,
    n=None,
    stream=False,
    stream_options=None,
    stop=None,
    max_tokens=None,
    max_completion_tokens=None,
    modalities=None,
    prediction=None,
    audio=None,
    presence_penalty=None,
    frequency_penalty=None,
    logit_bias=None,
    user=None,
    custom_llm_provider="",
    response_format=None,
    seed=None,
    tools=None,
    tool_choice=None,
    max_retries=None,
    logprobs=None,
    top_logprobs=None,
    extra_headers=None,
    api_version=None,
    parallel_tool_calls=None,
    drop_params=None,
    allowed_openai_params: Optional[List[str]] = None,
    reasoning_effort=None,
    verbosity=None,
    additional_drop_params=None,
    messages: Optional[List[AllMessageValues]] = None,
    thinking: Optional[AnthropicThinkingParam] = None,
    web_search_options: Optional[OpenAIWebSearchOptions] = None,
    safety_identifier: Optional[str] = None,
    base_model: Optional[str] = None,
    **kwargs,
):
    passed_params = locals().copy()
    special_params = passed_params.pop("kwargs")
    # Remove base_model from passed_params so it doesn't interfere with
    # non_default_params / _check_valid_arg — it's a routing hint, not an
    # OpenAI param.
    passed_params.pop("base_model", None)
    provider_config: Optional[BaseConfig] = None
    if custom_llm_provider is not None and custom_llm_provider in [
        provider.value for provider in LlmProviders
    ]:
        provider_config = ProviderConfigManager.get_provider_chat_config(
            model=model,
            provider=LlmProviders(custom_llm_provider),
            base_model=base_model,
        )
    non_default_params = pre_process_non_default_params(
        passed_params=passed_params,
        special_params=special_params,
        custom_llm_provider=custom_llm_provider,
        additional_drop_params=additional_drop_params,
        model=model,
        provider_config=provider_config,
    )
    optional_params = pre_process_optional_params(
        passed_params=passed_params,
        non_default_params=non_default_params,
        custom_llm_provider=custom_llm_provider,
    )

    def _check_valid_arg(supported_params: List[str]):
        """
        Check if the params passed to completion() are supported by the provider

        Args:
            supported_params: List[str] - supported params from the litellm config
        """
        verbose_logger.info(
            f"\nLiteLLM completion() model= {model}; provider = {custom_llm_provider}"
        )
        verbose_logger.debug(
            f"\nLiteLLM: Params passed to completion() {passed_params}"
        )
        verbose_logger.debug(
            f"\nLiteLLM: Non-Default params passed to completion() {non_default_params}"
        )
        unsupported_params = {}
        for k in non_default_params.keys():
            if k not in supported_params:
                if k == "user" or k == "stream_options" or k == "stream":
                    continue
                if k == "n" and n == 1:  # langchain sends n=1 as a default value
                    continue  # skip this param
                if (
                    k == "max_retries"
                ):  # TODO: This is a patch. We support max retries for OpenAI, Azure. For non OpenAI LLMs we need to add support for max retries
                    continue  # skip this param
                # Always keeps this in elif code blocks
                else:
                    unsupported_params[k] = non_default_params[k]

        if unsupported_params:
            if litellm.drop_params is True or (
                drop_params is not None and drop_params is True
            ):
                for k in unsupported_params.keys():
                    non_default_params.pop(k, None)
            else:
                raise UnsupportedParamsError(
                    status_code=500,
                    message=f"{custom_llm_provider} does not support parameters: {list(unsupported_params.keys())}, for model={model}. To drop these, set `litellm.drop_params=True` or for proxy:\n\n`litellm_settings:\n drop_params: true`\n. \n If you want to use these params dynamically send allowed_openai_params={list(unsupported_params.keys())} in your request.",
                )

    get_supported_openai_params = getattr(
        sys.modules[__name__], "get_supported_openai_params"
    )
    supported_params = get_supported_openai_params(
        model=model, custom_llm_provider=custom_llm_provider, base_model=base_model
    )
    if supported_params is None:
        supported_params = get_supported_openai_params(
            model=model, custom_llm_provider="openai"
        )

    supported_params = supported_params or []
    allowed_openai_params = allowed_openai_params or []
    supported_params.extend(allowed_openai_params)

    _check_valid_arg(
        supported_params=supported_params or [],
    )
    ## raise exception if provider doesn't support passed in param
    if custom_llm_provider == "anthropic":
        ## check if unsupported param passed in
        optional_params = litellm.AnthropicConfig().map_openai_params(
            model=model,
            non_default_params=non_default_params,
            optional_params=optional_params,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "anthropic_text":
        optional_params = litellm.AnthropicTextConfig().map_openai_params(
            model=model,
            non_default_params=non_default_params,
            optional_params=optional_params,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
        optional_params = litellm.AnthropicTextConfig().map_openai_params(
            model=model,
            non_default_params=non_default_params,
            optional_params=optional_params,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )

    elif custom_llm_provider == "cohere_chat" or custom_llm_provider == "cohere":
        # handle cohere params
        optional_params = litellm.CohereChatConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "triton":
        optional_params = litellm.TritonConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=drop_params if drop_params is not None else False,
        )

    elif custom_llm_provider == "maritalk":
        optional_params = litellm.MaritalkConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "replicate":
        optional_params = litellm.ReplicateConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "predibase":
        optional_params = litellm.PredibaseConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "huggingface":
        optional_params = litellm.HuggingFaceChatConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "together_ai":
        optional_params = litellm.TogetherAIConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "vertex_ai" and (
        model in litellm.vertex_chat_models
        or model in litellm.vertex_code_chat_models
        or model in litellm.vertex_text_models
        or model in litellm.vertex_code_text_models
        or model in litellm.vertex_language_models
        or model in litellm.vertex_vision_models
    ):
        optional_params = litellm.VertexGeminiConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )

    elif custom_llm_provider == "gemini":
        optional_params = litellm.GoogleAIStudioGeminiConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "vertex_ai_beta" or (
        custom_llm_provider == "vertex_ai" and "gemini" in model
    ):
        optional_params = litellm.VertexGeminiConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif litellm.VertexAIAnthropicConfig.is_supported_model(
        model=model, custom_llm_provider=custom_llm_provider
    ):
        optional_params = litellm.VertexAIAnthropicConfig().map_openai_params(
            model=model,
            non_default_params=non_default_params,
            optional_params=optional_params,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "vertex_ai":
        if model in litellm.vertex_mistral_models:
            if "codestral" in model:
                optional_params = (
                    litellm.CodestralTextCompletionConfig().map_openai_params(
                        model=model,
                        non_default_params=non_default_params,
                        optional_params=optional_params,
                        drop_params=(
                            drop_params
                            if drop_params is not None and isinstance(drop_params, bool)
                            else False
                        ),
                    )
                )
            else:
                optional_params = litellm.MistralConfig().map_openai_params(
                    model=model,
                    non_default_params=non_default_params,
                    optional_params=optional_params,
                    drop_params=(
                        drop_params
                        if drop_params is not None and isinstance(drop_params, bool)
                        else False
                    ),
                )
        elif model in litellm.vertex_ai_ai21_models:
            optional_params = litellm.VertexAIAi21Config().map_openai_params(
                non_default_params=non_default_params,
                optional_params=optional_params,
                model=model,
                drop_params=(
                    drop_params
                    if drop_params is not None and isinstance(drop_params, bool)
                    else False
                ),
            )
        elif provider_config is not None:
            optional_params = provider_config.map_openai_params(
                non_default_params=non_default_params,
                optional_params=optional_params,
                model=model,
                drop_params=(
                    drop_params
                    if drop_params is not None and isinstance(drop_params, bool)
                    else False
                ),
            )
        else:  # use generic openai-like param mapping
            optional_params = litellm.VertexAILlama3Config().map_openai_params(
                non_default_params=non_default_params,
                optional_params=optional_params,
                model=model,
                drop_params=(
                    drop_params
                    if drop_params is not None and isinstance(drop_params, bool)
                    else False
                ),
            )

    elif custom_llm_provider == "sagemaker":
        # temperature, top_p, n, stream, stop, max_tokens, n, presence_penalty default to None
        optional_params = litellm.SagemakerConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "bedrock":
        BedrockModelInfo = getattr(sys.modules[__name__], "BedrockModelInfo")
        bedrock_route = BedrockModelInfo.get_bedrock_route(model)
        bedrock_base_model = BedrockModelInfo.get_base_model(model)
        if bedrock_route == "converse" or bedrock_route == "converse_like":
            optional_params = litellm.AmazonConverseConfig().map_openai_params(
                model=model,
                non_default_params=non_default_params,
                optional_params=optional_params,
                drop_params=(
                    drop_params
                    if drop_params is not None and isinstance(drop_params, bool)
                    else False
                ),
            )
        elif bedrock_route == "openai":
            optional_params = litellm.AmazonBedrockOpenAIConfig().map_openai_params(
                model=model,
                non_default_params=non_default_params,
                optional_params=optional_params,
                drop_params=(
                    drop_params
                    if drop_params is not None and isinstance(drop_params, bool)
                    else False
                ),
            )
        elif "anthropic" in bedrock_base_model and bedrock_route == "invoke":
            if (
                bedrock_base_model
                in litellm.AmazonAnthropicConfig.get_legacy_anthropic_model_names()
            ):
                optional_params = litellm.AmazonAnthropicConfig().map_openai_params(
                    non_default_params=non_default_params,
                    optional_params=optional_params,
                    model=model,
                    drop_params=(
                        drop_params
                        if drop_params is not None and isinstance(drop_params, bool)
                        else False
                    ),
                )
            else:
                optional_params = (
                    litellm.AmazonAnthropicClaudeConfig().map_openai_params(
                        non_default_params=non_default_params,
                        optional_params=optional_params,
                        model=model,
                        drop_params=(
                            drop_params
                            if drop_params is not None and isinstance(drop_params, bool)
                            else False
                        ),
                    )
                )
        elif provider_config is not None:
            optional_params = provider_config.map_openai_params(
                non_default_params=non_default_params,
                optional_params=optional_params,
                model=model,
                drop_params=(
                    drop_params
                    if drop_params is not None and isinstance(drop_params, bool)
                    else False
                ),
            )
            if bedrock_route == "claude_platform":
                optional_params = BedrockModelInfo.map_claude_platform_auth_params(
                    passed_params=passed_params, optional_params=optional_params
                )
    elif custom_llm_provider == "cloudflare":
        optional_params = litellm.CloudflareChatConfig().map_openai_params(
            model=model,
            non_default_params=non_default_params,
            optional_params=optional_params,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "ollama":
        optional_params = litellm.OllamaConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "ollama_chat":
        optional_params = litellm.OllamaChatConfig().map_openai_params(
            model=model,
            non_default_params=non_default_params,
            optional_params=optional_params,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "nlp_cloud":
        optional_params = litellm.NLPCloudConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )

    elif custom_llm_provider == "petals":
        optional_params = litellm.PetalsConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "deepinfra":
        optional_params = litellm.DeepInfraConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "perplexity" and provider_config is not None:
        optional_params = provider_config.map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "mistral" or custom_llm_provider == "codestral":
        optional_params = litellm.MistralConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "text-completion-codestral":
        optional_params = litellm.CodestralTextCompletionConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )

    elif custom_llm_provider == "text-completion-inception":
        optional_params = litellm.InceptionTextCompletionConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )

    elif custom_llm_provider == "databricks":
        optional_params = litellm.DatabricksConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "nvidia_nim":
        optional_params = litellm.NvidiaNimConfig().map_openai_params(
            model=model,
            non_default_params=non_default_params,
            optional_params=optional_params,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "cerebras":
        optional_params = litellm.CerebrasConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "xai":
        optional_params = litellm.XAIChatConfig().map_openai_params(
            model=model,
            non_default_params=non_default_params,
            optional_params=optional_params,
        )
    elif custom_llm_provider == "ai21_chat" or custom_llm_provider == "ai21":
        optional_params = litellm.AI21ChatConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "fireworks_ai":
        optional_params = litellm.FireworksAIConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "volcengine":
        optional_params = litellm.VolcEngineConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "hosted_vllm":
        optional_params = litellm.HostedVLLMChatConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "vllm":
        optional_params = litellm.VLLMConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "groq":
        optional_params = litellm.GroqChatConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "bedrock_mantle":
        optional_params = litellm.BedrockMantleChatConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "deepseek":
        optional_params = litellm.DeepSeekChatConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "openrouter":
        optional_params = litellm.OpenrouterConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "watsonx":
        optional_params = litellm.IBMWatsonXChatConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
        # WatsonX-text param check
        for param in passed_params.keys():
            if litellm.IBMWatsonXAIConfig().is_watsonx_text_param(param):
                raise ValueError(
                    f"LiteLLM now defaults to Watsonx's `/text/chat` endpoint. Please use the `watsonx_text` provider instead, to call the `/text/generation` endpoint. Param: {param}"
                )
    elif custom_llm_provider == "watsonx_text":
        optional_params = litellm.IBMWatsonXAIConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "openai":
        optional_params = litellm.OpenAIConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "nebius":
        optional_params = litellm.NebiusConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    elif custom_llm_provider == "azure":
        _azure_detection_model = base_model or model
        if litellm.AzureOpenAIO1Config().is_o_series_model(
            model=_azure_detection_model
        ):
            optional_params = litellm.AzureOpenAIO1Config().map_openai_params(
                non_default_params=non_default_params,
                optional_params=optional_params,
                model=_azure_detection_model,
                drop_params=(
                    drop_params
                    if drop_params is not None and isinstance(drop_params, bool)
                    else False
                ),
            )
        elif litellm.AzureOpenAIGPT5Config.is_model_gpt_5_model(
            model=_azure_detection_model
        ):
            optional_params = litellm.AzureOpenAIGPT5Config().map_openai_params(
                non_default_params=non_default_params,
                optional_params=optional_params,
                model=_azure_detection_model,
                drop_params=(
                    drop_params
                    if drop_params is not None and isinstance(drop_params, bool)
                    else False
                ),
            )
        else:
            verbose_logger.debug(
                "Azure optional params - api_version: api_version={}, litellm.api_version={}, os.environ['AZURE_API_VERSION']={}".format(
                    api_version, litellm.api_version, get_secret("AZURE_API_VERSION")
                )
            )
            api_version = (
                api_version
                or litellm.api_version
                or get_secret("AZURE_API_VERSION")
                or litellm.AZURE_DEFAULT_API_VERSION
            )
            optional_params = litellm.AzureOpenAIConfig().map_openai_params(
                non_default_params=non_default_params,
                optional_params=optional_params,
                model=_azure_detection_model,
                api_version=api_version,  # type: ignore
                drop_params=(
                    drop_params
                    if drop_params is not None and isinstance(drop_params, bool)
                    else False
                ),
            )
    elif provider_config is not None:
        optional_params = provider_config.map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    else:  # assume passing in params for openai-like api
        optional_params = litellm.OpenAILikeChatConfig().map_openai_params(
            non_default_params=non_default_params,
            optional_params=optional_params,
            model=model,
            drop_params=(
                drop_params
                if drop_params is not None and isinstance(drop_params, bool)
                else False
            ),
        )
    # if user passed in non-default kwargs for specific providers/models, pass them along
    optional_params = add_provider_specific_params_to_optional_params(
        optional_params=optional_params,
        passed_params=passed_params,
        custom_llm_provider=custom_llm_provider,
        openai_params=list(DEFAULT_CHAT_COMPLETION_PARAM_VALUES.keys()),
        additional_drop_params=additional_drop_params,
    )
    print_verbose(f"Final returned optional params: {optional_params}")
    optional_params = _apply_openai_param_overrides(
        optional_params=optional_params,
        non_default_params=non_default_params,
        allowed_openai_params=allowed_openai_params,
    )

    # Apply nested drops from additional_drop_params
    if additional_drop_params:
        is_nested_path = getattr(sys.modules[__name__], "is_nested_path")
        delete_nested_value = getattr(sys.modules[__name__], "delete_nested_value")
        nested_paths = [p for p in additional_drop_params if is_nested_path(p)]
        for path in nested_paths:
            optional_params = delete_nested_value(optional_params, path)

    return optional_params

