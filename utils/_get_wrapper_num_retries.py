
def _get_wrapper_num_retries(
    kwargs: Dict[str, Any], exception: Exception
) -> Tuple[Optional[int], Dict[str, Any]]:
    """
    Get the number of retries from the kwargs and the retry policy.
    Used for the wrapper functions.
    """

    num_retries = kwargs.get("num_retries", None)
    if num_retries is None:
        num_retries = litellm.num_retries
    if kwargs.get("retry_policy", None):
        get_num_retries_from_retry_policy = getattr(
            sys.modules[__name__], "get_num_retries_from_retry_policy"
        )
        reset_retry_policy = getattr(sys.modules[__name__], "reset_retry_policy")
        retry_policy_num_retries = get_num_retries_from_retry_policy(
            exception=exception,
            retry_policy=kwargs.get("retry_policy"),
        )
        kwargs["retry_policy"] = reset_retry_policy()
        if retry_policy_num_retries is not None:
            num_retries = retry_policy_num_retries

    return num_retries, kwargs

