
def _update_logging(kwargs: dict, provider: str, operation: str) -> None:
    logging_obj = kwargs.get("litellm_logging_obj")
    if logging_obj is None:
        return
    logging_obj.update_from_kwargs(
        kwargs=kwargs,
        model=f"{provider}/{operation}",
        optional_params={},
        litellm_params={"litellm_call_id": kwargs.get("litellm_call_id")},
        custom_llm_provider=provider,
    )

