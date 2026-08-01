
def get_llm_provider(
    model: str,
    custom_llm_provider: Optional[str] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
    litellm_params: Optional[GenericLiteLLMParams] = None,
) -> Tuple[str, str, Optional[str], Optional[str]]:
    """
    Returns the provider for a given model name - e.g. 'azure/chatgpt-v-2' -> 'azure'

    For router -> Can also give the whole litellm param dict -> this function will extract the relevant details

    Raises Error - if unable to map model to a provider

    Return model, custom_llm_provider, dynamic_api_key, api_base
    """
    try:
        # Early validation - model is required
        if model is None:
            raise ValueError(
                "model parameter is required but was None. Please provide a valid model name."
            )

        if litellm.LiteLLMProxyChatConfig._should_use_litellm_proxy_by_default(
            litellm_params=cast(Optional[LiteLLM_Params], litellm_params)
        ):
            return litellm.LiteLLMProxyChatConfig.litellm_proxy_get_custom_llm_provider_info(
                model=model, api_base=api_base, api_key=api_key
            )

        ## IF LITELLM PARAMS GIVEN ##
        if litellm_params:
            if custom_llm_provider is None and api_base is None and api_key is None:
                custom_llm_provider = litellm_params.custom_llm_provider
                api_base = litellm_params.api_base
                api_key = litellm_params.api_key

        dynamic_api_key = None
        # check if llm provider provided
        # AZURE AI-Studio Logic - Azure AI Studio supports AZURE/Cohere
        # If User passes azure/command-r-plus -> we should send it to cohere_chat/command-r-plus
        if model.split("/", 1)[0] == "azure":
            if _is_non_openai_azure_model(model):
                custom_llm_provider = "openai"
                return model, custom_llm_provider, dynamic_api_key, api_base

        ### Handle cases when custom_llm_provider is set to cohere/command-r-plus but it should use cohere_chat route
        model, custom_llm_provider = handle_cohere_chat_model_custom_llm_provider(
            model, custom_llm_provider
        )

        model, custom_llm_provider = handle_anthropic_text_model_custom_llm_provider(
            model, custom_llm_provider
        )

        if custom_llm_provider and (
            model.split("/")[0] != custom_llm_provider
        ):  # handle scenario where model="azure/*" and custom_llm_provider="azure"
            model = custom_llm_provider + "/" + model

        # OpenRouter: when the router/proxy already set custom_llm_provider,
        # the model may still carry LiteLLM's "openrouter/" routing prefix.
        # Native IDs like "openrouter/auto" must stay intact for the API; IDs
        # like "openrouter/anthropic/claude-3.5-sonnet" must become
        # "anthropic/claude-3.5-sonnet" (OpenRouter expects provider/model).
        if custom_llm_provider == "openrouter" and model.startswith("openrouter/"):
            remainder = model[len("openrouter/") :]
            if "/" in remainder:
                return remainder, custom_llm_provider, dynamic_api_key, api_base
            return model, custom_llm_provider, dynamic_api_key, api_base

        # Check JSON-configured providers FIRST (before enum-based provider_list)
        provider_prefix = model.split("/", 1)[0]
        if len(model.split("/")) > 1 and JSONProviderRegistry.exists(provider_prefix):
            return _get_openai_compatible_provider_info(
                model=model,
                api_base=api_base,
                api_key=api_key,
                dynamic_api_key=dynamic_api_key,
                litellm_params=litellm_params,
            )

        # check if llm provider part of model name

        if (
            model.split("/", 1)[0] in litellm.provider_list
            and model.split("/", 1)[0] not in litellm.model_list_set
            and len(model.split("/"))
            > 1  # handle edge case where user passes in `litellm --model mistral` https://github.com/BerriAI/litellm/issues/1351
        ):
            return _get_openai_compatible_provider_info(
                model=model,
                api_base=api_base,
                api_key=api_key,
                dynamic_api_key=dynamic_api_key,
                litellm_params=litellm_params,
            )
        elif model.split("/", 1)[0] in litellm.provider_list:
            custom_llm_provider = model.split("/", 1)[0]
            model = model.split("/", 1)[1]
            if api_base is not None and not isinstance(api_base, str):
                raise Exception(
                    "api base needs to be a string. api_base={}".format(api_base)
                )
            if dynamic_api_key is not None and not isinstance(dynamic_api_key, str):
                raise Exception(
                    "dynamic_api_key needs to be a string. Got type={}".format(
                        type(dynamic_api_key).__name__
                    )
                )
            return model, custom_llm_provider, dynamic_api_key, api_base
        # check if api base is a known openai compatible endpoint
        if api_base:
            for endpoint in litellm.openai_compatible_endpoints:
                if _endpoint_matches_api_base(endpoint, api_base):
                    if endpoint == "api.perplexity.ai":
                        custom_llm_provider = "perplexity"
                        dynamic_api_key = get_secret_str("PERPLEXITYAI_API_KEY")
                    elif endpoint == "api.endpoints.anyscale.com/v1":
                        custom_llm_provider = "anyscale"
                        dynamic_api_key = get_secret_str("ANYSCALE_API_KEY")
                    elif endpoint == "api.deepinfra.com/v1/openai":
                        custom_llm_provider = "deepinfra"
                        dynamic_api_key = get_secret_str("DEEPINFRA_API_KEY")
                    elif endpoint == "api.mistral.ai/v1":
                        custom_llm_provider = "mistral"
                        dynamic_api_key = get_secret_str("MISTRAL_API_KEY")
                    elif endpoint == "api.groq.com/openai/v1":
                        custom_llm_provider = "groq"
                        dynamic_api_key = get_secret_str("GROQ_API_KEY")
                    elif endpoint == "https://integrate.api.nvidia.com/v1":
                        custom_llm_provider = "nvidia_nim"
                        dynamic_api_key = get_secret_str("NVIDIA_NIM_API_KEY")
                    elif endpoint == "https://api.cerebras.ai/v1":
                        custom_llm_provider = "cerebras"
                        dynamic_api_key = get_secret_str("CEREBRAS_API_KEY")
                    elif endpoint == "https://inference.baseten.co/v1":
                        custom_llm_provider = "baseten"
                        dynamic_api_key = get_secret_str("BASETEN_API_KEY")
                    elif endpoint == "https://api.sambanova.ai/v1":
                        custom_llm_provider = "sambanova"
                        dynamic_api_key = get_secret_str("SAMBANOVA_API_KEY")
                    elif endpoint == "https://api.ai21.com/studio/v1":
                        custom_llm_provider = "ai21_chat"
                        dynamic_api_key = get_secret_str("AI21_API_KEY")
                    elif endpoint == "codestral.mistral.ai/v1/chat/completions":
                        custom_llm_provider = "codestral"
                        dynamic_api_key = get_secret_str("CODESTRAL_API_KEY")
                    elif endpoint == "codestral.mistral.ai/v1/fim/completions":
                        custom_llm_provider = "text-completion-codestral"
                        dynamic_api_key = get_secret_str("CODESTRAL_API_KEY")
                    elif endpoint == "app.empower.dev/api/v1":
                        custom_llm_provider = "empower"
                        dynamic_api_key = get_secret_str("EMPOWER_API_KEY")
                    elif endpoint == "api.deepseek.com/v1":
                        custom_llm_provider = "deepseek"
                        dynamic_api_key = get_secret_str("DEEPSEEK_API_KEY")
                    elif endpoint == "ollama.com":
                        custom_llm_provider = "ollama"
                        dynamic_api_key = get_secret_str("OLLAMA_API_KEY")
                    elif endpoint == "https://api.friendli.ai/serverless/v1":
                        custom_llm_provider = "friendliai"
                        dynamic_api_key = get_secret_str(
                            "FRIENDLIAI_API_KEY"
                        ) or get_secret("FRIENDLI_TOKEN")
                    elif endpoint == "api.galadriel.com/v1":
                        custom_llm_provider = "galadriel"
                        dynamic_api_key = get_secret_str("GALADRIEL_API_KEY")
                    elif endpoint == "https://api.llama.com/compat/v1":
                        custom_llm_provider = "meta_llama"
                        dynamic_api_key = api_key or get_secret_str("LLAMA_API_KEY")
                    elif endpoint == "https://api.featherless.ai/v1":
                        custom_llm_provider = "featherless_ai"
                        dynamic_api_key = get_secret_str("FEATHERLESS_AI_API_KEY")
                    elif endpoint == litellm.NscaleConfig.API_BASE_URL:
                        custom_llm_provider = "nscale"
                        dynamic_api_key = litellm.NscaleConfig.get_api_key()
                    elif endpoint == "dashscope-intl.aliyuncs.com/compatible-mode/v1":
                        custom_llm_provider = "dashscope"
                        dynamic_api_key = get_secret_str("DASHSCOPE_API_KEY")
                    elif endpoint == "https://api-inference.modelscope.cn/v1":
                        custom_llm_provider = "modelscope"
                        dynamic_api_key = get_secret_str("MODELSCOPE_API_KEY")
                    elif endpoint == "api.moonshot.ai/v1":
                        custom_llm_provider = "moonshot"
                        dynamic_api_key = get_secret_str("MOONSHOT_API_KEY")
                    elif (
                        endpoint == "api.minimax.io/anthropic"
                        or endpoint == "api.minimaxi.com/anthropic"
                    ):
                        custom_llm_provider = "minimax"
                        dynamic_api_key = get_secret_str("MINIMAX_API_KEY")
                    elif (
                        endpoint == "api.minimax.io/v1"
                        or endpoint == "api.minimaxi.com/v1"
                    ):
                        custom_llm_provider = "minimax"
                        dynamic_api_key = get_secret_str("MINIMAX_API_KEY")
                    elif endpoint == "platform.publicai.co/v1":
                        custom_llm_provider = "publicai"
                        dynamic_api_key = get_secret_str("PUBLICAI_API_KEY")
                    elif endpoint == "https://api.synthetic.new/openai/v1":
                        custom_llm_provider = "synthetic"
                        dynamic_api_key = get_secret_str("SYNTHETIC_API_KEY")
                    elif endpoint == "https://api.stima.tech/v1":
                        custom_llm_provider = "apertis"
                        dynamic_api_key = get_secret_str("STIMA_API_KEY")
                    elif endpoint == "https://nano-gpt.com/api/v1":
                        custom_llm_provider = "nano-gpt"
                        dynamic_api_key = get_secret_str("NANOGPT_API_KEY")
                    elif endpoint == "https://api.poe.com/v1":
                        custom_llm_provider = "poe"
                        dynamic_api_key = get_secret_str("POE_API_KEY")
                    elif endpoint == "https://llm.chutes.ai/v1/":
                        custom_llm_provider = "chutes"
                        dynamic_api_key = get_secret_str("CHUTES_API_KEY")
                    elif endpoint == "https://api.v0.dev/v1":
                        custom_llm_provider = "v0"
                        dynamic_api_key = get_secret_str("V0_API_KEY")
                    elif endpoint == "https://api.lambda.ai/v1":
                        custom_llm_provider = "lambda_ai"
                        dynamic_api_key = get_secret_str("LAMBDA_API_KEY")
                    elif endpoint == "https://api.inceptionlabs.ai/v1":
                        custom_llm_provider = "inception"
                        dynamic_api_key = get_secret_str("INCEPTION_API_KEY")
                    elif endpoint == "https://api.hyperbolic.xyz/v1":
                        custom_llm_provider = "hyperbolic"
                        dynamic_api_key = get_secret_str("HYPERBOLIC_API_KEY")
                    elif endpoint == "https://ai-gateway.vercel.sh/v1":
                        custom_llm_provider = "vercel_ai_gateway"
                        dynamic_api_key = get_secret_str("VERCEL_AI_GATEWAY_API_KEY")
                    elif endpoint == "https://api.inference.wandb.ai/v1":
                        custom_llm_provider = "wandb"
                        dynamic_api_key = get_secret_str("WANDB_API_KEY")
                    elif endpoint == "https://pinstripes.io/v1":
                        custom_llm_provider = "pinstripes"
                        dynamic_api_key = get_secret_str("PINSTRIPES_API_KEY")

                    if api_base is not None and not isinstance(api_base, str):
                        raise Exception(
                            "api base needs to be a string. api_base={}".format(
                                api_base
                            )
                        )
                    if dynamic_api_key is not None and not isinstance(
                        dynamic_api_key, str
                    ):
                        raise Exception(
                            "dynamic_api_key needs to be a string. dynamic_api_key={}".format(
                                dynamic_api_key
                            )
                        )
                    return model, custom_llm_provider, dynamic_api_key, api_base  # type: ignore

        # check if model in known model provider list  -> for huggingface models, raise exception as they don't have a fixed provider (can be togetherai, anyscale, baseten, runpod, et.)
        ## openai - chatcompletion + text completion
        if (
            model in litellm.open_ai_chat_completion_models
            or "ft:gpt-3.5-turbo" in model
            or "ft:gpt-4" in model  # catches ft:gpt-4-0613, ft:gpt-4o
            or model in litellm.openai_image_generation_models
            or model.startswith("gpt-image")
            or model in litellm.openai_video_generation_models
        ):
            custom_llm_provider = "openai"
        elif model in litellm.open_ai_text_completion_models:
            custom_llm_provider = "text-completion-openai"
        ## anthropic
        elif model in litellm.anthropic_models:
            if litellm.AnthropicTextConfig._is_anthropic_text_model(model):
                custom_llm_provider = "anthropic_text"
            else:
                custom_llm_provider = "anthropic"
        ## anthropic - pattern-based matching for future Claude models
        elif _matches_claude_model_pattern(model):
            custom_llm_provider = "anthropic"
        ## cohere
        elif model in litellm.cohere_models or model in litellm.cohere_embedding_models:
            custom_llm_provider = "cohere"
        ## cohere chat models
        elif model in litellm.cohere_chat_models:
            custom_llm_provider = "cohere_chat"
        ## replicate
        elif model in litellm.replicate_models or (
            ":" in model and len(model) > REPLICATE_MODEL_NAME_WITH_ID_LENGTH
        ):
            model_parts = model.split(":")
            if (
                len(model_parts) > 1
                and len(model_parts[1]) == REPLICATE_MODEL_NAME_WITH_ID_LENGTH
            ):  ## checks if model name has a 64 digit code - e.g. "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"
                custom_llm_provider = "replicate"
            elif model in litellm.replicate_models:
                custom_llm_provider = "replicate"
        ## openrouter
        elif model in litellm.openrouter_models:
            custom_llm_provider = "openrouter"
        ## maritalk
        elif model in litellm.maritalk_models:
            custom_llm_provider = "maritalk"
        ## vertex - text + chat + language (gemini) models
        elif (
            model in litellm.vertex_chat_models
            or model in litellm.vertex_code_chat_models
            or model in litellm.vertex_text_models
            or model in litellm.vertex_code_text_models
            or model in litellm.vertex_language_models
            or model in litellm.vertex_embedding_models
            or model in litellm.vertex_vision_models
            or model in litellm.vertex_ai_image_models
            or model in litellm.vertex_ai_video_models
        ):
            custom_llm_provider = "vertex_ai"
        ## ai21
        elif model in litellm.ai21_chat_models or model in litellm.ai21_models:
            custom_llm_provider = "ai21_chat"
            api_base = (
                api_base
                or get_secret("AI21_API_BASE")
                or "https://api.ai21.com/studio/v1"
            )  # type: ignore
            dynamic_api_key = api_key or get_secret("AI21_API_KEY")
        ## aleph_alpha
        elif model in litellm.aleph_alpha_models:
            custom_llm_provider = "aleph_alpha"
        ## baseten
        elif model in litellm.baseten_models:
            custom_llm_provider = "baseten"
        ## nlp_cloud
        elif model in litellm.nlp_cloud_models:
            custom_llm_provider = "nlp_cloud"
        ## petals
        elif model in litellm.petals_models:
            custom_llm_provider = "petals"
        ## bedrock
        elif (
            model in litellm.bedrock_models
            or model in litellm.bedrock_embedding_models
            or model in litellm.bedrock_converse_models
        ):
            custom_llm_provider = "bedrock"
        elif model in litellm.watsonx_models:
            custom_llm_provider = "watsonx"
        # openai embeddings
        elif model in litellm.open_ai_embedding_models:
            custom_llm_provider = "openai"
        elif model in litellm.empower_models:
            custom_llm_provider = "empower"
        elif model in litellm.gradient_ai_models:
            custom_llm_provider = "gradient_ai"
        elif model == "*":
            custom_llm_provider = "openai"
        # bytez models
        elif model.startswith("bytez/"):
            custom_llm_provider = "bytez"
        elif model.startswith("lemonade/"):
            custom_llm_provider = "lemonade"
        elif model.startswith("heroku/"):
            custom_llm_provider = "heroku"
        # cometapi models
        elif model.startswith("cometapi/"):
            custom_llm_provider = "cometapi"
        elif model.startswith("oci/"):
            custom_llm_provider = "oci"
        elif model.startswith("compactifai/"):
            custom_llm_provider = "compactifai"
        elif model.startswith("ovhcloud/"):
            custom_llm_provider = "ovhcloud"
        elif model.startswith("lemonade/"):
            custom_llm_provider = "lemonade"
        elif model.startswith("clarifai/"):
            custom_llm_provider = "clarifai"
        elif model.startswith("amazon_nova"):
            custom_llm_provider = "amazon_nova"
        elif model.startswith("sap/"):
            custom_llm_provider = "sap"
        if not custom_llm_provider:
            if litellm.suppress_debug_info is False:
                print()  # noqa: T201
                print(  # noqa: T201
                    "\033[1;31mProvider List: https://docs.litellm.ai/docs/providers\033[0m"
                )
                print()  # noqa: T201
            error_str = f"LLM Provider NOT provided. Pass in the LLM provider you are trying to call. You passed model={model}\n Pass model as E.g. For 'Huggingface' inference endpoints pass in `completion(model='huggingface/starcoder',..)` Learn more: https://docs.litellm.ai/docs/providers"
            # maps to openai.NotFoundError, this is raised when openai does not recognize the llm
            raise litellm.exceptions.BadRequestError(  # type: ignore
                message=error_str,
                model=model,
                response=None,
                llm_provider="",
            )
        if api_base is not None and not isinstance(api_base, str):
            raise Exception(
                "api base needs to be a string. api_base={}".format(api_base)
            )
        if dynamic_api_key is not None and not isinstance(dynamic_api_key, str):
            raise Exception(
                "dynamic_api_key needs to be a string. dynamic_api_key={}".format(
                    dynamic_api_key
                )
            )
        return model, custom_llm_provider, dynamic_api_key, api_base
    except Exception as e:
        if isinstance(e, litellm.exceptions.BadRequestError):
            raise e
        else:
            error_str = (
                f"GetLLMProvider Exception - {str(e)}\n\noriginal model: {model}"
            )
            raise litellm.exceptions.BadRequestError(  # type: ignore
                message=f"GetLLMProvider Exception - {str(e)}\n\noriginal model: {model}",
                model=model,
                response=None,
                llm_provider="",
            )

