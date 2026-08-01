
def _is_multimodal_input(input: GeminiEmbeddingInput) -> bool:
    """
    Check if the input contains multimodal data (data URIs, file references,
    GCS URLs, or nested lists for combined embeddings).

    Args:
        input: GeminiEmbeddingInput — str, List[str], or List[List[str]] for combined embeddings

    Returns:
        bool: True if any element is multimodal or a nested list
    """
    if isinstance(input, str):
        return _is_multimodal_element(input)

    for element in input:
        if isinstance(element, list):
            if any(
                _is_multimodal_element(sub) for sub in element if isinstance(sub, str)
            ):
                return True
        elif isinstance(element, str) and _is_multimodal_element(element):
            return True

    return False

