
def completion_with_retries(*args, **kwargs):
    """
    Executes a litellm.completion() with 3 retries
    """
    try:
        import tenacity
    except Exception as e:
        raise Exception(
            f"tenacity import failed please run `pip install tenacity`. Error{e}"
        )

    num_retries = kwargs.pop("num_retries", 3)
    # reset retries in .completion()
    kwargs["max_retries"] = 0
    kwargs["num_retries"] = 0
    retry_strategy: Literal["exponential_backoff_retry", "constant_retry"] = kwargs.pop(
        "retry_strategy", "constant_retry"
    )  # type: ignore
    original_function = kwargs.pop("original_function", completion)
    if retry_strategy == "exponential_backoff_retry":
        retryer = tenacity.Retrying(
            wait=tenacity.wait_exponential(multiplier=1, max=10),
            stop=tenacity.stop_after_attempt(num_retries),
            reraise=True,
        )
    else:
        retryer = tenacity.Retrying(
            stop=tenacity.stop_after_attempt(num_retries), reraise=True
        )
    return retryer(original_function, *args, **kwargs)

