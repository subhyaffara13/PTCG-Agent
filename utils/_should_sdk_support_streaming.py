
def _should_sdk_support_streaming(
    custom_llm_provider: Optional[Union[FileContentProvider, str]],
) -> bool:
    """
    Return whether file content streaming is supported for the provider.
    """
    return custom_llm_provider in OPENAI_COMPATIBLE_BATCH_AND_FILES_PROVIDERS

