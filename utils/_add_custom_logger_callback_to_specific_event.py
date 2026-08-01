
def _add_custom_logger_callback_to_specific_event(
    callback: str, logging_event: Literal["success", "failure"]
) -> None:
    """
    Add a custom logger callback to the specific event
    """
    from litellm import _custom_logger_compatible_callbacks_literal
    from litellm.litellm_core_utils.litellm_logging import (
        _init_custom_logger_compatible_class,
    )

    if callback not in litellm._known_custom_logger_compatible_callbacks:
        verbose_logger.debug(
            f"Callback {callback} is not a valid custom logger compatible callback. Known list - {litellm._known_custom_logger_compatible_callbacks}"
        )
        return

    callback_class = _init_custom_logger_compatible_class(
        cast(_custom_logger_compatible_callbacks_literal, callback),
        internal_usage_cache=None,
        llm_router=None,
    )

    if callback_class:
        if (
            logging_event == "success"
            and _custom_logger_class_exists_in_success_callbacks(callback_class)
            is False
        ):
            litellm.logging_callback_manager.add_litellm_success_callback(
                callback_class
            )
            litellm.logging_callback_manager.add_litellm_async_success_callback(
                callback_class
            )
            if callback in litellm.success_callback:
                litellm.success_callback.remove(
                    callback
                )  # remove the string from the callback list
            if callback in litellm._async_success_callback:
                litellm._async_success_callback.remove(
                    callback
                )  # remove the string from the callback list
        elif (
            logging_event == "failure"
            and _custom_logger_class_exists_in_failure_callbacks(callback_class)
            is False
        ):
            litellm.logging_callback_manager.add_litellm_failure_callback(
                callback_class
            )
            litellm.logging_callback_manager.add_litellm_async_failure_callback(
                callback_class
            )
            if callback in litellm.failure_callback:
                litellm.failure_callback.remove(
                    callback
                )  # remove the string from the callback list
            if callback in litellm._async_failure_callback:
                litellm._async_failure_callback.remove(
                    callback
                )  # remove the string from the callback list

