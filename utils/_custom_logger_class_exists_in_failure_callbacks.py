
def _custom_logger_class_exists_in_failure_callbacks(
    callback_class: "CustomLogger",
) -> bool:
    """
    Returns True if an instance of the custom logger exists in litellm.failure_callback or litellm._async_failure_callback

    e.g if `LangfusePromptManagement` is passed in, it will return True if an instance of `LangfusePromptManagement` exists in litellm.failure_callback or litellm._async_failure_callback

    Prevents double adding a custom logger callback to the litellm callbacks
    """
    return any(
        isinstance(cb, type(callback_class))
        for cb in litellm.failure_callback + litellm._async_failure_callback
    )

