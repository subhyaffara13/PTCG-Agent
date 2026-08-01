
def _get_router_memory_stats(llm_router) -> Dict[str, Any]:
    """Get memory usage statistics for LiteLLM router."""
    litellm_router_memory: Dict[str, Any] = {}
    try:
        if llm_router is not None:
            # Model list memory size
            if hasattr(llm_router, "model_list") and llm_router.model_list:
                model_list_size = sys.getsizeof(llm_router.model_list)
                litellm_router_memory["model_list"] = {
                    "num_models": len(llm_router.model_list),
                    "size_bytes": model_list_size,
                    "size_mb": round(model_list_size / (1024 * 1024), 4),
                }

            # Model names set
            if hasattr(llm_router, "model_names") and llm_router.model_names:
                model_names_size = sys.getsizeof(llm_router.model_names)
                litellm_router_memory["model_names_set"] = {
                    "num_model_groups": len(llm_router.model_names),
                    "size_bytes": model_names_size,
                    "size_mb": round(model_names_size / (1024 * 1024), 4),
                }

            # Deployment names list
            if hasattr(llm_router, "deployment_names") and llm_router.deployment_names:
                deployment_names_size = sys.getsizeof(llm_router.deployment_names)
                litellm_router_memory["deployment_names"] = {
                    "num_deployments": len(llm_router.deployment_names),
                    "size_bytes": deployment_names_size,
                    "size_mb": round(deployment_names_size / (1024 * 1024), 4),
                }

            # Deployment latency map
            if (
                hasattr(llm_router, "deployment_latency_map")
                and llm_router.deployment_latency_map
            ):
                latency_map_size = sys.getsizeof(llm_router.deployment_latency_map)
                litellm_router_memory["deployment_latency_map"] = {
                    "num_tracked_deployments": len(llm_router.deployment_latency_map),
                    "size_bytes": latency_map_size,
                    "size_mb": round(latency_map_size / (1024 * 1024), 4),
                }

            # Fallback configuration
            if hasattr(llm_router, "fallbacks") and llm_router.fallbacks:
                fallbacks_size = sys.getsizeof(llm_router.fallbacks)
                litellm_router_memory["fallbacks"] = {
                    "num_fallback_configs": len(llm_router.fallbacks),
                    "size_bytes": fallbacks_size,
                    "size_mb": round(fallbacks_size / (1024 * 1024), 4),
                }

            # Total router object size
            router_obj_size = sys.getsizeof(llm_router)
            litellm_router_memory["router_object"] = {
                "size_bytes": router_obj_size,
                "size_mb": round(router_obj_size / (1024 * 1024), 4),
            }

        else:
            litellm_router_memory = {"note": "Router not initialized"}
    except Exception as e:
        verbose_proxy_logger.debug(f"Error getting router memory info: {e}")
        litellm_router_memory = {"error": str(e)}

    return litellm_router_memory

