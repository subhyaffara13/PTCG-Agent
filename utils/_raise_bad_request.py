
def _raise_bad_request(message: str, model: str) -> NoReturn:
    import litellm

    raise litellm.BadRequestError(
        message=message,
        model=model,
        llm_provider="reducto",
    )

