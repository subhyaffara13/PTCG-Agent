
def _should_defer_streaming_cache_hit_callbacks(*, kwargs: Dict[str, Any]) -> bool:
    """
    When stream=True, do not run success callbacks at cache-hit time.

    Cached chat/text completion replay uses CustomStreamWrapper; cached Responses
    replay uses CachedResponsesAPIStreamingIterator. Both invoke logging success
    handlers when the stream finishes; firing them here too would double-count
    spend and callback records.
    """
    return kwargs.get("stream", False) is True

