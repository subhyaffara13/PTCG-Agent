from typing import Any, Dict, Optional

def _resolve_embedding_config_from_router(
    embedding_model: str, llm_router
) -> Optional[Dict[str, Any]]:
    """
    Resolve embedding config from router's config-defined models.

    Config-defined models (from proxy_config.yaml) are stored in the router's model_list,
    not in the database. This function looks up the model in the router and extracts
    api_key, api_base, and api_version from the deployment's litellm_params.

    Args:
        embedding_model: The embedding model string (e.g., "text-embedding-ada-002" or "azure/text-embedding-3-large")
        llm_router: The LiteLLM router instance

    Returns:
        Dictionary with api_key, api_base, and api_version if model found, None otherwise
    """
    if not embedding_model or llm_router is None:
        return None

    # Extract model name candidates - could be "text-embedding-ada-002" or "azure/text-embedding-3-large"
    # Try exact match first, then try without provider prefix
    model_name_candidates = [embedding_model]
    if "/" in embedding_model:
        # If it has a provider prefix, also try without it
        _, model_name = embedding_model.split("/", 1)
        model_name_candidates.append(model_name)

    # Try to find model in router
    for model_name in model_name_candidates:
        try:
            # Try to get deployment by model group name (model_name in config)
            deployment = llm_router.get_deployment_by_model_group_name(
                model_group_name=model_name
            )

            if deployment is not None and deployment.litellm_params is not None:
                litellm_params = deployment.litellm_params

                # Build embedding config from model params
                embedding_config: Dict[str, Any] = {}

                # Extract api_key
                api_key = getattr(litellm_params, "api_key", None)
                if api_key:
                    # Handle os.environ/ prefix
                    if isinstance(api_key, str) and api_key.startswith("os.environ/"):
                        api_key = get_secret(api_key)
                    embedding_config["api_key"] = api_key

                # Extract api_base
                api_base = getattr(litellm_params, "api_base", None)
                if api_base:
                    # Handle os.environ/ prefix
                    if isinstance(api_base, str) and api_base.startswith("os.environ/"):
                        api_base = get_secret(api_base)
                    embedding_config["api_base"] = api_base

                # Extract api_version
                api_version = getattr(litellm_params, "api_version", None)
                if api_version:
                    embedding_config["api_version"] = api_version

                project_id = getattr(litellm_params, "project_id", None)
                if project_id:
                    embedding_config["project_id"] = project_id

                # Only return config if we have at least api_key or api_base
                if embedding_config:
                    verbose_proxy_logger.debug(
                        f"Resolved embedding config from router model {model_name}: {list(embedding_config.keys())}"
                    )
                    return embedding_config
        except Exception as e:
            verbose_proxy_logger.debug(
                f"Error resolving embedding config from router for model {model_name}: {str(e)}"
            )
            continue

    return None

