from typing import Optional, Tuple

def _resolve_model_for_cost_lookup(model: str) -> Tuple[str, Optional[str]]:
    """
    Resolve a model name (which may be a router alias/model_group) to the
    underlying litellm model name for cost lookup.

    Args:
        model: The model name from the request (could be a router alias like 'e-model-router'
               or an actual model name like 'azure_ai/gpt-4')

    Returns:
        Tuple of (resolved_model_name, custom_llm_provider)
        - resolved_model_name: The actual model name to use for cost lookup
        - custom_llm_provider: The provider if resolved from router, None otherwise
    """
    from litellm.proxy.proxy_server import llm_router

    custom_llm_provider: Optional[str] = None

    # Try to resolve from router if available
    if llm_router is not None:
        try:
            # Get deployments for this model name (handles aliases, wildcards, etc.)
            deployments = llm_router.get_model_list(model_name=model)

            if deployments and len(deployments) > 0:
                first_deployment = deployments[0]
                litellm_params = first_deployment.get("litellm_params", {})
                model_info = first_deployment.get("model_info", {})

                # Check base_model first (needed for Azure custom deployment names)
                base_model = model_info.get("base_model") or litellm_params.get(
                    "base_model"
                )
                if base_model:
                    verbose_proxy_logger.debug(
                        f"Resolved model '{model}' to base_model '{base_model}' from router"
                    )
                    custom_llm_provider = litellm_params.get("custom_llm_provider")
                    return (
                        str(base_model),
                        (
                            str(custom_llm_provider)
                            if custom_llm_provider is not None
                            else None
                        ),
                    )

                resolved_model = litellm_params.get("model")

                if resolved_model:
                    verbose_proxy_logger.debug(
                        f"Resolved model '{model}' to '{resolved_model}' from router"
                    )
                    custom_llm_provider = litellm_params.get("custom_llm_provider")
                    return (
                        str(resolved_model),
                        (
                            str(custom_llm_provider)
                            if custom_llm_provider is not None
                            else None
                        ),
                    )
        except Exception as e:
            verbose_proxy_logger.debug(
                f"Could not resolve model '{model}' from router: {e}"
            )

    # Return original model if not resolved
    return model, custom_llm_provider

