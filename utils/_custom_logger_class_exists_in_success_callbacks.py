
def _custom_logger_class_exists_in_success_callbacks(
    callback_class: "CustomLogger",
) -> bool:
    """
    Returns True if an instance of the custom logger exists in litellm.success_callback or litellm._async_success_callback

    e.g if `LangfusePromptManagement` is passed in, it will return True if an instance of `LangfusePromptManagement` exists in litellm.success_callback or litellm._async_success_callback

    Prevents double adding a custom logger callback to the litellm callbacks
    """
    return any(
        isinstance(cb, type(callback_class))
        for cb in litellm.success_callback + litellm._async_success_callback
    )

