
def _extract_cache_params() -> Dict[str, Any]:
    """
    Safely extracts and cleans cache parameters.

    The health check UI needs to display specific cache parameters, to show users how they set up their cache.

    eg.
        {
            "host": "localhost",
            "port": 6379,
            "redis_kwargs": {"db": 0},
            "namespace": "test",
        }

    Returns:
        Dict containing cleaned and masked cache parameters
    """
    if litellm.cache is None:
        return {}
    try:
        cache_params = vars(litellm.cache.cache)
        cleaned_params = (
            HealthCheckCacheParams(**cache_params).model_dump() if cache_params else {}
        )
        return masker.mask_dict(cleaned_params)
    except (AttributeError, TypeError) as e:
        verbose_proxy_logger.debug(f"Error extracting cache params: {str(e)}")
        return {}

