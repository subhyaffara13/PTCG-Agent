import sys
from typing import Any, Dict

def _get_cache_memory_stats(
    user_api_key_cache, llm_router, proxy_logging_obj, redis_usage_cache
) -> Dict[str, Any]:
    """Calculate memory usage for all caches."""
    cache_stats: Dict[str, Any] = {}
    try:
        # User API key cache
        user_cache_size = sys.getsizeof(user_api_key_cache.in_memory_cache.cache_dict)
        user_ttl_size = sys.getsizeof(user_api_key_cache.in_memory_cache.ttl_dict)
        cache_stats["user_api_key_cache"] = {
            "num_items": len(user_api_key_cache.in_memory_cache.cache_dict),
            "cache_dict_size_bytes": user_cache_size,
            "ttl_dict_size_bytes": user_ttl_size,
            "total_size_mb": round(
                (user_cache_size + user_ttl_size) / (1024 * 1024), 2
            ),
        }

        # Router cache
        if llm_router is not None:
            router_cache_size = sys.getsizeof(
                llm_router.cache.in_memory_cache.cache_dict
            )
            router_ttl_size = sys.getsizeof(llm_router.cache.in_memory_cache.ttl_dict)
            cache_stats["llm_router_cache"] = {
                "num_items": len(llm_router.cache.in_memory_cache.cache_dict),
                "cache_dict_size_bytes": router_cache_size,
                "ttl_dict_size_bytes": router_ttl_size,
                "total_size_mb": round(
                    (router_cache_size + router_ttl_size) / (1024 * 1024), 2
                ),
            }

        # Proxy logging cache
        logging_cache_size = sys.getsizeof(
            proxy_logging_obj.internal_usage_cache.dual_cache.in_memory_cache.cache_dict
        )
        logging_ttl_size = sys.getsizeof(
            proxy_logging_obj.internal_usage_cache.dual_cache.in_memory_cache.ttl_dict
        )
        cache_stats["proxy_logging_cache"] = {
            "num_items": len(
                proxy_logging_obj.internal_usage_cache.dual_cache.in_memory_cache.cache_dict
            ),
            "cache_dict_size_bytes": logging_cache_size,
            "ttl_dict_size_bytes": logging_ttl_size,
            "total_size_mb": round(
                (logging_cache_size + logging_ttl_size) / (1024 * 1024), 2
            ),
        }

        # Redis cache info
        if redis_usage_cache is not None:
            cache_stats["redis_usage_cache"] = {
                "enabled": True,
                "cache_type": type(redis_usage_cache).__name__,
            }
            # Try to get Redis connection pool info if available
            try:
                if (
                    hasattr(redis_usage_cache, "redis_client")
                    and redis_usage_cache.redis_client
                ):
                    if hasattr(redis_usage_cache.redis_client, "connection_pool"):
                        pool_info = redis_usage_cache.redis_client.connection_pool  # type: ignore
                        cache_stats["redis_usage_cache"]["connection_pool"] = {
                            "max_connections": (
                                pool_info.max_connections
                                if hasattr(pool_info, "max_connections")
                                else None
                            ),
                            "connection_class": (
                                pool_info.connection_class.__name__
                                if hasattr(pool_info, "connection_class")
                                else None
                            ),
                        }
            except Exception as e:
                verbose_proxy_logger.debug(f"Error getting Redis pool info: {e}")
        else:
            cache_stats["redis_usage_cache"] = {"enabled": False}

    except Exception as e:
        verbose_proxy_logger.debug(f"Error calculating cache stats: {e}")
        cache_stats["error"] = str(e)

    return cache_stats

