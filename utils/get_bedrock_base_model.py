
def get_bedrock_base_model(model: str) -> str:
    """
    Get the base model from the given model name.

    Handle model names like:
    - "us.meta.llama3-2-11b-instruct-v1:0" -> "meta.llama3-2-11b-instruct-v1"
    - "bedrock/converse/model" -> "model"
    - "anthropic.claude-3-5-sonnet-20241022-v2:0:51k" -> "anthropic.claude-3-5-sonnet-20241022-v2:0"
    - "bedrock/nova-2/arn:aws:..." -> "amazon.nova-2-custom"
    - "bedrock/nova/arn:aws:..." -> "amazon.nova-custom"
    """
    # Detect nova spec prefixes before stripping them
    stripped = model
    for rp in ["bedrock/converse/", "bedrock/", "converse/"]:
        if stripped.startswith(rp):
            stripped = stripped[len(rp) :]
            break
    if stripped.startswith("nova-2/"):
        return "amazon.nova-2-custom"
    elif stripped.startswith("nova/"):
        return "amazon.nova-custom"

    model = strip_bedrock_routing_prefix(model)
    model = extract_model_name_from_bedrock_arn(model)
    model = strip_bedrock_throughput_suffix(model)

    potential_region = model.split(".", 1)[0]
    alt_potential_region = model.split("/", 1)[0]

    if potential_region in get_bedrock_cross_region_inference_regions():
        return model.split(".", 1)[1]
    elif (
        alt_potential_region in _get_all_bedrock_regions()
        and len(model.split("/", 1)) > 1
    ):
        return model.split("/", 1)[1]

    return model

