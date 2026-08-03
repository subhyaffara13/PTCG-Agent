from typing import Optional, Tuple

def _get_openai_compatible_provider_info(
    model: str,
    api_base: Optional[str],
    api_key: Optional[str],
    dynamic_api_key: Optional[str],
    litellm_params: Optional[GenericLiteLLMParams] = None,
) -> Tuple[str, str, Optional[str], Optional[str]]:
    """
    Returns:
        Tuple[str, str, Optional[str], Optional[str]]:
            model: str
            custom_llm_provider: str
            dynamic_api_key: Optional[str]
            api_base: Optional[str]
    """

    custom_llm_provider = model.split("/", 1)[0]
    model = model.split("/", 1)[1]

    # Check JSON providers FIRST (before hardcoded ones)
    from litellm.llms.openai_like.dynamic_config import create_config_class
    from litellm.llms.openai_like.json_loader import JSONProviderRegistry

    if JSONProviderRegistry.exists(custom_llm_provider):
        provider_config = JSONProviderRegistry.get(custom_llm_provider)
        if provider_config is None:
            raise ValueError(f"Provider {custom_llm_provider} not found")
        config_class = create_config_class(provider_config)
        api_base, dynamic_api_key = config_class()._get_openai_compatible_provider_info(
            api_base, api_key
        )
        return model, custom_llm_provider, dynamic_api_key, api_base

    if custom_llm_provider == "perplexity":
        # perplexity is openai compatible, we just need to set this to custom_openai and have the api_base be https://api.perplexity.ai
        (
            api_base,
            dynamic_api_key,
        ) = litellm.PerplexityChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "aiohttp_openai":
        return model, "aiohttp_openai", api_key, api_base
    elif custom_llm_provider == "anyscale":
        # anyscale is openai compatible, we just need to set this to custom_openai and have the api_base be https://api.endpoints.anyscale.com/v1
        api_base = api_base or get_secret_str("ANYSCALE_API_BASE") or "https://api.endpoints.anyscale.com/v1"  # type: ignore
        dynamic_api_key = api_key or get_secret_str("ANYSCALE_API_KEY")
    elif custom_llm_provider == "deepinfra":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.DeepInfraConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "empower":
        api_base = (
            api_base
            or get_secret("EMPOWER_API_BASE")
            or "https://app.empower.dev/api/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("EMPOWER_API_KEY")
    elif custom_llm_provider == "groq":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.GroqChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "bedrock_mantle":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.BedrockMantleChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key, litellm_params=litellm_params, model=model
        )
    elif custom_llm_provider == "nvidia_nim":
        # nvidia_nim is openai compatible, we just need to set this to custom_openai and have the api_base be https://api.endpoints.anyscale.com/v1
        api_base = (
            api_base
            or get_secret("NVIDIA_NIM_API_BASE")
            or "https://integrate.api.nvidia.com/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("NVIDIA_NIM_API_KEY")
    elif custom_llm_provider == "nvidia_riva":
        # NVIDIA Riva is gRPC-based; api_base must be a host:port like
        # `grpc.nvcf.nvidia.com:443` or `localhost:50051`. There is no
        # public-default endpoint, so we do not fill one in here.
        api_base = api_base or get_secret_str("NVIDIA_RIVA_API_BASE")  # type: ignore
        # Fall back to NVIDIA_NIM_API_KEY because users running both NVCF
        # services typically reuse the same nvapi-* key.
        dynamic_api_key = (
            api_key
            or get_secret_str("NVIDIA_RIVA_API_KEY")
            or get_secret_str("NVIDIA_NIM_API_KEY")
        )
    elif custom_llm_provider == "soniox":
        api_base = (
            api_base or get_secret_str("SONIOX_API_BASE") or "https://api.soniox.com"
        )
        dynamic_api_key = api_key or get_secret_str("SONIOX_API_KEY")
    elif custom_llm_provider == "cerebras":
        api_base = (
            api_base or get_secret("CEREBRAS_API_BASE") or "https://api.cerebras.ai/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("CEREBRAS_API_KEY")
    elif custom_llm_provider == "baseten":
        # Use BasetenConfig to determine the appropriate API base URL
        if api_base is None:
            api_base = litellm.BasetenConfig.get_api_base_for_model(model)
        else:
            api_base = (
                api_base
                or get_secret_str("BASETEN_API_BASE")
                or "https://inference.baseten.co/v1"
            )
        dynamic_api_key = api_key or get_secret_str("BASETEN_API_KEY")
    elif custom_llm_provider == "sambanova":
        api_base = (
            api_base
            or get_secret("SAMBANOVA_API_BASE")
            or "https://api.sambanova.ai/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("SAMBANOVA_API_KEY")
    elif custom_llm_provider == "meta_llama":
        api_base = (
            api_base
            or get_secret("LLAMA_API_BASE")
            or "https://api.llama.com/compat/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("LLAMA_API_KEY")
    elif custom_llm_provider == "nebius":
        api_base = (
            api_base
            or get_secret("NEBIUS_API_BASE")
            or "https://api.studio.nebius.ai/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("NEBIUS_API_KEY")
    elif custom_llm_provider == "ollama":
        api_base = (
            api_base or get_secret("OLLAMA_API_BASE") or "http://localhost:11434"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("OLLAMA_API_KEY")
    elif (custom_llm_provider == "ai21_chat") or (
        custom_llm_provider == "ai21" and model in litellm.ai21_chat_models
    ):
        api_base = (
            api_base or get_secret("AI21_API_BASE") or "https://api.ai21.com/studio/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("AI21_API_KEY")
        custom_llm_provider = "ai21_chat"
    elif custom_llm_provider == "volcengine":
        # volcengine is openai compatible, we just need to set this to custom_openai and have the api_base be https://api.endpoints.anyscale.com/v1
        api_base = (
            api_base
            or get_secret("VOLCENGINE_API_BASE")
            or "https://ark.cn-beijing.volces.com/api/v3"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("VOLCENGINE_API_KEY")
    elif custom_llm_provider == "codestral":
        # codestral is openai compatible, we just need to set this to custom_openai and have the api_base be https://codestral.mistral.ai/v1
        api_base = (
            api_base
            or get_secret("CODESTRAL_API_BASE")
            or "https://codestral.mistral.ai/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("CODESTRAL_API_KEY")
    elif custom_llm_provider == "hosted_vllm":
        # vllm is openai compatible, we just need to set this to custom_openai
        (
            api_base,
            dynamic_api_key,
        ) = litellm.HostedVLLMChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "llamafile":
        # llamafile is OpenAI compatible.
        (
            api_base,
            dynamic_api_key,
        ) = litellm.LlamafileChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "datarobot":
        # DataRobot is OpenAI compatible.
        (
            api_base,
            dynamic_api_key,
        ) = litellm.DataRobotConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "lm_studio":
        # lm_studio is openai compatible, we just need to set this to custom_openai
        (
            api_base,
            dynamic_api_key,
        ) = litellm.LMStudioChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "deepseek":
        # deepseek is openai compatible, we just need to set this to custom_openai and have the api_base be https://api.deepseek.com/v1
        api_base = (
            api_base
            or get_secret("DEEPSEEK_API_BASE")
            or "https://api.deepseek.com/beta"
        )  # type: ignore

        dynamic_api_key = api_key or get_secret_str("DEEPSEEK_API_KEY")
    elif custom_llm_provider == "fireworks_ai":
        # fireworks is openai compatible, we just need to set this to custom_openai and have the api_base be https://api.fireworks.ai/inference/v1
        (
            api_base,
            dynamic_api_key,
        ) = litellm.FireworksAIConfig()._get_openai_compatible_provider_info(
            api_base=api_base, api_key=api_key
        )
    elif custom_llm_provider == "azure_ai":
        (
            api_base,
            dynamic_api_key,
            custom_llm_provider,
        ) = litellm.AzureAIStudioConfig()._get_openai_compatible_provider_info(
            model, api_base, api_key, custom_llm_provider
        )
    elif custom_llm_provider == "github":
        api_base = (
            api_base
            or get_secret_str("GITHUB_API_BASE")
            or "https://models.inference.ai.azure.com"  # This is github's default base url
        )
        dynamic_api_key = api_key or get_secret_str("GITHUB_API_KEY")
    elif custom_llm_provider == "litellm_proxy":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.LiteLLMProxyChatConfig()._get_openai_compatible_provider_info(
            api_base=api_base, api_key=api_key
        )

    elif custom_llm_provider == "mistral":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.MistralConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "jina_ai":
        (
            custom_llm_provider,
            api_base,
            dynamic_api_key,
        ) = litellm.JinaAIEmbeddingConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "xai":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.XAIChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "zai":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.ZAIChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "together_ai":
        api_base = (
            api_base
            or get_secret_str("TOGETHER_AI_API_BASE")
            or "https://api.together.xyz/v1"
        )  # type: ignore
        dynamic_api_key = api_key or (
            get_secret_str("TOGETHER_API_KEY")
            or get_secret_str("TOGETHER_AI_API_KEY")
            or get_secret_str("TOGETHERAI_API_KEY")
            or get_secret_str("TOGETHER_AI_TOKEN")
        )
    elif custom_llm_provider == "friendliai":
        api_base = (
            api_base
            or get_secret("FRIENDLI_API_BASE")
            or "https://api.friendli.ai/serverless/v1"
        )  # type: ignore
        dynamic_api_key = (
            api_key
            or get_secret_str("FRIENDLIAI_API_KEY")
            or get_secret_str("FRIENDLI_TOKEN")
        )
    elif custom_llm_provider == "galadriel":
        api_base = (
            api_base
            or get_secret("GALADRIEL_API_BASE")
            or "https://api.galadriel.com/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("GALADRIEL_API_KEY")
    elif custom_llm_provider == "github_copilot":
        (
            api_base,
            dynamic_api_key,
            custom_llm_provider,
        ) = litellm.GithubCopilotConfig()._get_openai_compatible_provider_info(
            model, api_base, api_key, custom_llm_provider
        )
    elif custom_llm_provider == "chatgpt":
        (
            api_base,
            dynamic_api_key,
            custom_llm_provider,
        ) = litellm.ChatGPTConfig()._get_openai_compatible_provider_info(
            model, api_base, api_key, custom_llm_provider
        )
    elif custom_llm_provider == "novita":
        api_base = (
            api_base
            or get_secret("NOVITA_API_BASE")
            or "https://api.novita.ai/v3/openai"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("NOVITA_API_KEY")
    elif custom_llm_provider == "snowflake":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.SnowflakeConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "gradient_ai":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.GradientAIConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "featherless_ai":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.FeatherlessAIConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "nscale":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.NscaleConfig()._get_openai_compatible_provider_info(
            api_base=api_base, api_key=api_key
        )
    elif custom_llm_provider == "heroku":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.HerokuChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "dashscope":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.DashScopeChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "modelscope":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.ModelScopeChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "moonshot":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.MoonshotChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    # publicai is now handled by JSON config (see litellm/llms/openai_like/providers.json)
    elif custom_llm_provider == "docker_model_runner":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.DockerModelRunnerChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "v0":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.V0ChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "morph":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.MorphChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "lambda_ai":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.LambdaAIChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "inception":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.InceptionChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "hyperbolic":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.HyperbolicChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "vercel_ai_gateway":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.VercelAIGatewayConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "aiml":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.AIMLChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "wandb":
        api_base = (
            api_base
            or get_secret("WANDB_API_BASE")
            or "https://api.inference.wandb.ai/v1"
        )  # type: ignore
        dynamic_api_key = api_key or get_secret_str("WANDB_API_KEY")
    elif custom_llm_provider == "lemonade":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.LemonadeChatConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "clarifai":
        (
            api_base,
            dynamic_api_key,
        ) = litellm.ClarifaiConfig()._get_openai_compatible_provider_info(
            api_base, api_key
        )
    elif custom_llm_provider == "ragflow":
        full_model = f"ragflow/{model}"
        (
            api_base,
            dynamic_api_key,
            _,
        ) = litellm.RAGFlowConfig()._get_openai_compatible_provider_info(
            full_model, api_base, api_key, "ragflow"
        )
        model = full_model
    elif custom_llm_provider == "langgraph":
        # LangGraph is a custom provider, just need to set api_base
        api_base = (
            api_base or get_secret_str("LANGGRAPH_API_BASE") or "http://localhost:2024"
        )
        dynamic_api_key = api_key or get_secret_str("LANGGRAPH_API_KEY")
    elif custom_llm_provider == "manus":
        # Manus is OpenAI compatible for responses API
        api_base = (
            api_base or get_secret_str("MANUS_API_BASE") or "https://api.manus.im"
        )
        dynamic_api_key = api_key or get_secret_str("MANUS_API_KEY")

    if api_base is not None and not isinstance(api_base, str):
        raise Exception("api base needs to be a string. api_base={}".format(api_base))
    if dynamic_api_key is not None and not isinstance(dynamic_api_key, str):
        raise Exception(
            "dynamic_api_key needs to be a string. dynamic_api_key={}".format(
                dynamic_api_key
            )
        )
    if dynamic_api_key is None and api_key is not None:
        dynamic_api_key = api_key
    return model, custom_llm_provider, dynamic_api_key, api_base

