
def cost_router(call_type: CallTypes) -> Literal["cost_per_token", "cost_per_second"]:
    if call_type == CallTypes.atranscription or call_type == CallTypes.transcription:
        return "cost_per_second"
    else:
        return "cost_per_token"


def cost_router(
    model: str,
    custom_llm_provider: str,
    call_type: Union[Literal["embedding", "aembedding"], str],
) -> Literal["cost_per_character", "cost_per_token"]:
    """
    Route the cost calc to the right place, based on model/call_type/etc.

    Returns
        - str, the specific google cost calc function it should route to.
    """
    if custom_llm_provider == "vertex_ai" and (
        "claude" in model
        or "llama" in model
        or "mistral" in model
        or "jamba" in model
        or "codestral" in model
        or "gemma" in model
    ):
        return "cost_per_token"
    elif custom_llm_provider == "vertex_ai" and (
        call_type == "embedding" or call_type == "aembedding"
    ):
        return "cost_per_token"
    elif custom_llm_provider == "vertex_ai" and ("gemini-2" in model):
        return "cost_per_token"
    return "cost_per_character"

