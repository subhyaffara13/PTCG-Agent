
def litellm_to_list(embeds: litellm.EmbeddingResponse) -> list[list[float]]:
    """Convert a LiteLLM embedding response to a list of embeddings.

    :param embeds: The LiteLLM embedding response.
    :return: A list of embeddings.
    """
    if (
        not embeds
        or not isinstance(embeds, litellm.EmbeddingResponse)
        or not embeds.data
    ):
        raise ValueError("No embeddings found in LiteLLM embedding response.")
    return [x["embedding"] for x in embeds.data]

