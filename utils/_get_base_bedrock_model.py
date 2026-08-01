
def _get_base_bedrock_model(model_name) -> str:
    """
    Get the base model from the given model name.

    Handle model names like - "us.meta.llama3-2-11b-instruct-v1:0" -> "meta.llama3-2-11b-instruct-v1"
    AND "meta.llama3-2-11b-instruct-v1:0" -> "meta.llama3-2-11b-instruct-v1"
    """
    from litellm.llms.bedrock.common_utils import BedrockModelInfo

    return BedrockModelInfo.get_base_model(model_name)

