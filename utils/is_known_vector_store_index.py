
def is_known_vector_store_index(index_name: str) -> bool:
    """
    Returns True if the vector store index is in the llm_router vector store indexes
    """

    if litellm.vector_store_index_registry is None:
        return False
    return index_name in litellm.vector_store_index_registry.get_vector_store_indexes()

