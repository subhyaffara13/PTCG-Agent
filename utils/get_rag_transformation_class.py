
def get_rag_transformation_class(custom_llm_provider: str):
    """
    Get the appropriate RAG transformation class for a provider.

    Args:
        custom_llm_provider: The LLM provider name

    Returns:
        The transformation class for the provider, or None if not needed
    """
    if custom_llm_provider == "vertex_ai":
        from litellm.llms.vertex_ai.rag_engine.transformation import (
            VertexAIRAGTransformation,
        )

        return VertexAIRAGTransformation

    # OpenAI and Bedrock don't need special transformations
    return None

