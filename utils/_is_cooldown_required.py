
def _is_cooldown_required(
    litellm_router_instance: LitellmRouter,
    model_id: str,
    exception_status: Union[str, int],
    exception_str: Optional[str] = None,
) -> bool:
    """
    A function to determine if a cooldown is required based on the exception status.

    Parameters:
        model_id (str) The id of the model in the model list
        exception_status (Union[str, int]): The status of the exception.

    Returns:
        bool: True if a cooldown is required, False otherwise.
    """
    try:
        ignored_strings = ["APIConnectionError"]
        if (
            exception_str is not None
        ):  # don't cooldown on litellm api connection errors errors
            for ignored_string in ignored_strings:
                if ignored_string in exception_str:
                    return False

        if isinstance(exception_status, str):
            if len(exception_status) == 0:
                return False
            exception_status = int(exception_status)

        if exception_status >= 400 and exception_status < 500:
            if exception_status == 429:
                # Cool down 429 Rate Limit Errors
                return True

            elif exception_status == 401:
                # Cool down 401 Auth Errors
                return True

            elif exception_status == 408:
                return True

            elif exception_status == 404:
                return True

            else:
                # Do NOT cool down all other 4XX Errors
                return False

        else:
            # should cool down for all other errors
            return True

    except Exception:
        # Catch all - if any exceptions default to cooling down
        return True

