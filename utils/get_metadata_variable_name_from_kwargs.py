
def get_metadata_variable_name_from_kwargs(
    kwargs: dict,
) -> Literal["metadata", "litellm_metadata"]:
    """
    Helper to return what the "metadata" field should be called in the request data

    - New endpoints return `litellm_metadata`
    - Old endpoints return `metadata`

    Context:
    - LiteLLM used `metadata` as an internal field for storing metadata
    - OpenAI then started using this field for their metadata
    - LiteLLM is now moving to using `litellm_metadata` for our metadata
    """
    return "litellm_metadata" if "litellm_metadata" in kwargs else "metadata"


def get_metadata_variable_name_from_kwargs(
    kwargs: dict,
) -> Literal["metadata", "litellm_metadata"]:
    """
    Helper to return what the "metadata" field should be called in the request data

    - New endpoints return `litellm_metadata`
    - Old endpoints return `metadata`

    Context:
    - LiteLLM used `metadata` as an internal field for storing metadata
    - OpenAI then started using this field for their metadata
    - LiteLLM is now moving to using `litellm_metadata` for our metadata
    """
    return "litellm_metadata" if "litellm_metadata" in kwargs else "metadata"

