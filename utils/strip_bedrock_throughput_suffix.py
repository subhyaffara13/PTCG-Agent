
def strip_bedrock_throughput_suffix(model: str) -> str:
    """Strip throughput tier suffixes and context window suffixes from Bedrock model names."""
    import re

    # Pattern matches model:version:throughput where throughput is like 51k, 18k, etc.
    # Keep the model:version part, strip the :throughput suffix
    model = re.sub(r"(:\d+):\d+k$", r"\1", model)
    # Strip context window suffixes like [1m], [200k], etc.
    # e.g. "us.anthropic.claude-opus-4-6-v1[1m]" -> "us.anthropic.claude-opus-4-6-v1"
    model = re.sub(r"\[\w+\]$", "", model)
    return model

