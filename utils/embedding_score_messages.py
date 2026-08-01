
def embedding_score_messages(
    query: str,
    messages: List[dict],
    model: str,
    cache: Optional[DualCache] = None,
    embedding_model_params: Optional[Dict[str, Any]] = None,
) -> List[float]:
    """
    Score each message's semantic similarity to the query using embeddings.

    Parameters:
        query: The reference text to score against.
        messages: List of message dicts with "content" fields.
        model: The embedding model to use (e.g., "text-embedding-3-small").
        cache: Optional DualCache for cross-turn embedding caching.
        embedding_model_params: Optional additional kwargs forwarded to
            ``litellm.embedding()``.

    Returns:
        List of float scores (cosine similarity), one per message.
    """
    import litellm

    texts = [_truncate_text(query)]
    for msg in messages:
        texts.append(_truncate_text(_extract_content(msg)))

    # Filter out empty texts — replace with a placeholder to maintain indexing
    processed_texts = [t if t.strip() else "empty" for t in texts]

    kwargs: Dict[str, Any] = {
        "model": model,
        "input": processed_texts,
        "caching": cache is not None,
    }
    if embedding_model_params:
        kwargs = {**kwargs, **embedding_model_params}

    response = litellm.embedding(**kwargs)

    # Extract embedding vectors
    embeddings = [item["embedding"] for item in response.data]

    query_embedding = embeddings[0]
    scores: List[float] = []
    for i in range(1, len(embeddings)):
        scores.append(_cosine_similarity(query_embedding, embeddings[i]))

    return scores

