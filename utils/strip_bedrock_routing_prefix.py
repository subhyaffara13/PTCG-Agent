
def strip_bedrock_routing_prefix(model: str) -> str:
    """Strip LiteLLM routing prefixes from model name."""
    for prefix in ["bedrock/", "converse/", "invoke/", "openai/", "nova-2/", "nova/"]:
        if model.startswith(prefix):
            model = model.split("/", 1)[1]
    return model

