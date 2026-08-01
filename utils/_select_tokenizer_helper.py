
def _select_tokenizer_helper(model: str) -> SelectTokenizerResponse:
    if litellm.disable_hf_tokenizer_download is True:
        return _return_openai_tokenizer(model)

    try:
        result = _return_huggingface_tokenizer(model)
        if result is not None:
            return result
    except Exception as e:
        verbose_logger.debug(f"Error selecting tokenizer: {e}")

    # default - tiktoken
    return _return_openai_tokenizer(model)

