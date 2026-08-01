
def get_provider_helper(provider: PROVIDER_OR_POLICY_T | None, task: str, model: str | None) -> TaskProviderHelper:
    """Get provider helper instance by name and task.

    Args:
        provider (`str`, *optional*): name of the provider, or "auto" to automatically select the provider for the model.
        task (`str`): Name of the task
        model (`str`, *optional*): Name of the model
    Returns:
        TaskProviderHelper: Helper instance for the specified provider and task

    Raises:
        ValueError: If provider or task is not supported
    """

    if (model is None and provider in (None, "auto")) or (
        model is not None and model.startswith(("http://", "https://"))
    ):
        provider = "hf-inference"

    if provider is None:
        logger.info(
            "No provider specified for task `conversational`. Defaulting to server-side auto routing."
            if task == "conversational"
            else "Defaulting to 'auto' which will select the first provider available for the model, sorted by the user's order in https://hf.co/settings/inference-providers."
        )
        provider = "auto"

    if provider == "auto":
        if model is None:
            raise ValueError("Specifying a model is required when provider is 'auto'")
        if task == "conversational":
            # Special case: we have a dedicated auto-router for conversational models. No need to fetch provider mapping.
            return CONVERSATIONAL_AUTO_ROUTER

        provider_mapping = _fetch_inference_provider_mapping(model)
        provider = next(iter(provider_mapping)).provider

    provider_tasks = PROVIDERS.get(provider)  # type: ignore
    if provider_tasks is None:
        raise ValueError(
            f"Provider '{provider}' not supported. Available values: 'auto' or any provider from {list(PROVIDERS.keys())}."
            "Passing 'auto' (default value) will automatically select the first provider available for the model, sorted "
            "by the user's order in https://hf.co/settings/inference-providers."
        )

    if task not in provider_tasks:
        raise ValueError(
            f"Task '{task}' not supported for provider '{provider}'. Available tasks: {list(provider_tasks.keys())}"
        )
    return provider_tasks[task]

