
def get_bedrock_chat_config(model: str):
    """
    Helper function to get the appropriate Bedrock chat config based on model and route.

    Args:
        model: The model name/identifier

    Returns:
        The appropriate Bedrock config class instance
    """
    bedrock_route = BedrockModelInfo.get_bedrock_route(model)
    bedrock_invoke_provider = litellm.BedrockLLM.get_bedrock_invoke_provider(
        model=model
    )
    base_model = BedrockModelInfo.get_base_model(model)

    # Handle explicit routes first
    if bedrock_route == "claude_platform":
        return litellm.BedrockClaudePlatformConfig()
    elif bedrock_route == "converse" or bedrock_route == "converse_like":
        return litellm.AmazonConverseConfig()
    elif bedrock_route == "openai":
        return litellm.AmazonBedrockOpenAIConfig()
    elif bedrock_route == "agent":
        from litellm.llms.bedrock.chat.invoke_agent.transformation import (
            AmazonInvokeAgentConfig,
        )

        return AmazonInvokeAgentConfig()
    elif bedrock_route == "agentcore":
        from litellm.llms.bedrock.chat.agentcore.transformation import (
            AmazonAgentCoreConfig,
        )

        return AmazonAgentCoreConfig()
    elif bedrock_route == "mantle":
        from litellm.llms.bedrock.chat.mantle.transformation import (
            AmazonMantleConfig,
        )

        return AmazonMantleConfig()

    # Handle provider-specific configs
    if bedrock_invoke_provider == "amazon":
        return litellm.AmazonTitanConfig()
    elif bedrock_invoke_provider == "anthropic":
        if (
            base_model
            in litellm.AmazonAnthropicConfig.get_legacy_anthropic_model_names()
        ):
            return litellm.AmazonAnthropicConfig()
        else:
            return litellm.AmazonAnthropicClaudeConfig()
    elif bedrock_invoke_provider == "meta" or bedrock_invoke_provider == "llama":
        return litellm.AmazonLlamaConfig()
    elif bedrock_invoke_provider == "ai21":
        return litellm.AmazonAI21Config()
    elif bedrock_invoke_provider == "cohere":
        return litellm.AmazonCohereConfig()
    elif bedrock_invoke_provider == "mistral":
        return litellm.AmazonMistralConfig()
    elif bedrock_invoke_provider == "moonshot":
        return litellm.AmazonMoonshotConfig()
    elif bedrock_invoke_provider == "deepseek_r1":
        return litellm.AmazonDeepSeekR1Config()
    elif bedrock_invoke_provider == "nova":
        return litellm.AmazonInvokeNovaConfig()
    elif bedrock_invoke_provider == "qwen3":
        return litellm.AmazonQwen3Config()
    elif bedrock_invoke_provider == "qwen2":
        return litellm.AmazonQwen2Config()
    elif bedrock_invoke_provider == "twelvelabs":
        return litellm.AmazonTwelveLabsPegasusConfig()
    else:
        return litellm.AmazonInvokeConfig()

