
def is_claude_4_5_on_bedrock(model: str) -> bool:
    """
    Check if the model is a Claude 4.5 model on Bedrock.
    Claude 4.5 models support prompt caching with '5m' and '1h' TTL on Bedrock.
    """
    model_lower = model.lower()
    claude_4_5_patterns = [
        "sonnet-4.5",
        "sonnet_4.5",
        "sonnet-4-5",
        "sonnet_4_5",
        "haiku-4.5",
        "haiku_4.5",
        "haiku-4-5",
        "haiku_4_5",
        "opus-4.5",
        "opus_4.5",
        "opus-4-5",
        "opus_4_5",
        "sonnet-4.6",
        "sonnet_4.6",
        "sonnet-4-6",
        "sonnet_4_6",
        "opus-4.6",
        "opus_4.6",
        "opus-4-6",
        "opus_4_6",
        "opus-4.7",
        "opus_4.7",
        "opus-4-7",
        "opus_4_7",
    ]
    return any(pattern in model_lower for pattern in claude_4_5_patterns)

